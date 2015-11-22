#-*- coding:utf-8 -*-
from scrapy.spider import Spider
from scrapy import Request, log
from scrapy.http import FormRequest
from zuoyehezi.items import ZItem
from zuoyehezi.items import Image
from bs4 import BeautifulSoup, UnicodeDammit
from bs4.element import NavigableString
import mysql.connector

import urlparse
import json
import urllib
import uuid
import os, re, time, random


# Initialization.
interface_url = "/Interface.aspx?url=" # seems to be interface btw front/back-end.
assignment_url = "/Assignment.aspx?url="
login_suffix = "@php/v1_user/teacher/login?source=webTeahcer&version=2.4.0"
main_url = "http://www.zuoyehezi.com"
cookienameList = [
                  '5lSrFqJA8W/BMizviIthB4qdfYWwHLCcOauAOHfrxf7WHw5S/rOr/Kl8yHtaGsW1',   # 初中英语
                  '/DQPDPQ9GPZorPPGPde+3ogXOw3zbbu5bCe+8+WveLO696oxcyxUqd96oVJTfyuE',   # 高中数学
                  '1HUuLSP7HSqJ4NyK1I0qMTHHr7Rxmz2bVJ3FRYFrO%2FOS6YF8mmNsqNbreKvmqebU', # 高中英语
                  'GkLJW7sRsxtg6zKEK4bQWApwflkAGRZQOSzsoODaKy5AJmbR0Vt+pCfg+i51FwSz',   # 初中数学
                 ]

# store images in directory `images`
img_dir = "images"

subjectType = [u"初中英语", u"高中数学"]
# subjectType = [u"高中英语", u""] # just for test

startIdx =  [1351, 3] # 1351 for junior eng, 3 for senior math 
lastIdx =   [1442, 15] # 1442 for junior eng, 205 for senior math



# get the idx range of every subject. only English currently.
def getRange(idx):
    # "0": "初中英语", "1":"高中数学"
    return startIdx[idx], lastIdx[idx]

class ZSpider(Spider):
    name = "ZSpider"
    start_urls = []
    dict_all = {}
    # allowed_domains = ["knowbox.cn"]

    # isntead of __init__, it can pass parameters.
    def start_requests(self):
        for i in range(len(subjectType)):
            tmp_url = "@php/v1_tiku/knowledge/list?source=webTeacher&token=%s&version=2.4.0" % cookienameList[i]
            url = main_url + interface_url + urllib.quote(tmp_url, safe='')
            yield Request(url = url, callback = self.parse, meta = {"subject": i})

    def getDesc(self, subject_id, ID):
        desc = ""
        d = self.dict_all[subject_id]
        idx = 0
        while idx != ID:
            for i in range(len(d)):
                item = d[i]
                idx = int(item["knowID"])
                if idx < ID:
                    if i == len(d) - 1:
                        d = d[i]["list"]
                    continue
                elif idx > ID:
                    desc += d[i-1]["knowledgeName"] + " > "
                    d = d[i-1]["list"]
                    break
                else:
                    desc += d[i]["knowledgeName"]
                    return desc

        return ''

    def parse(self, response):

        subject_id = response.meta["subject"]
        content = json.loads(response.body)
        self.dict_all[subject_id] = content["data"]["list"]

        cookiename = cookienameList[subject_id] # cookie: knowbox_teacherToken.
        ID = 0                  # id for question list.
        questionType =  '-1'    # -1: all, 0: choice, 1:multi-choice, 2: answer, 5: cloze.
        collectType =   '0'     # undefined / 0 / 1, function unknown.
        outType =       '0'     # undefined / 0 / 2, function unknown.
        pagesize =      '10'    # questions per page
        pagenum =       '0'     # pagination    num.    
        start =         startIdx[subject_id]
        end =           lastIdx[subject_id]

        if start == 0 and end == 0:
            return
        for ID in range(start, end+1):
            if ID == 1427:      # an exception for crawling!
                continue
            tmp_url = "@php/v1_tiku/knowledge/question?source=webTeacher&from=kb&token=%s&version=2.4.0&knowledge_id=%s&question_type=%s&collect=%s&out=%s&page_size=%s&page_num=%s" % \
                      (cookiename, ID, questionType, collectType, outType, pagesize, pagenum)
            
            question_url = main_url + interface_url + urllib.quote(tmp_url, safe='')
            qList = question_url.split("%26")
            qList[2] = "token%3D" + random.choice(cookienameList)
            question_url = "%26".join(qList)
            desc = self.getDesc(subject_id, ID)
            

            # analysis and store
            self.logger.info('Start crawling list %d page 0', ID)
            yield Request(url = question_url, callback = self.parse_list, \
                          meta = {"list_id": ID, "page_id": 0, "subject": subject_id, "desc": desc})

    def parse_list(self, response):
        # randomize the cookie name. 
        question_url = response.url
        qList = question_url.split("%26")
        qList[2] = "token%3D" + random.choice(cookienameList)
        question_url = "%26".join(qList)

        page_id = response.meta["page_id"]
        list_id = response.meta["list_id"]
        content = json.loads(response.body)
        code = content["code"]

        # if get nothing.
        if code == 20014:
            self.logger.info("Oops! Crawler going too fast!")
            question_url = response.url
            qList = question_url.split("%26")
            qList[2] = "token%3D" + random.choice(cookienameList)
            question_url = "%26".join(qList)
            yield Request(question_url, callback = self.parse_list, \
                          meta = {"list_id": list_id, "page_id": page_id, \
                                  "subject": response.meta["subject"], "desc": response.meta["desc"]})
            return
        if code != 99999:
            print "*****"
            print question_url
            print "*****"
            self.logger.warning('Unknown error when crawling list {}, page {}, code {}'.format(list_id, page_id, code))
            return
        if content["data"]["list"] == []:
            self.logger.info('PageInfo: No data exists when crawling list {}, page {}'.format(list_id, page_id))
            return 

        q_l = content["data"]["list"]
        for i in q_l:
            item = ZItem()
            item["description"] = response.meta["desc"]
            item["subject"] = response.meta["subject"]
            item["questionType"] = i["questionType"]
            item["questionID"] = i["questionID"]
            item["questionNo"] = i["questionNo"]
            # process: in case of images. same below.
            temp, item["content"] = self.process(i["content"])
            for x, y in temp:
                yield Request(url = x, callback = self.storeImage,  meta={"id": y, "desc": response.meta["desc"]})
            temp, item["rightAnswer"] = self.process(i["rightAnswer"])
            for x, y in temp:
                yield Request(url = x, callback = self.storeImage,  meta={"id": y, "desc": response.meta["desc"]})
            temp, item["answerExplain"] = self.process(i["answerExplain"])
            for x, y in temp:
                yield Request(url = x, callback = self.storeImage,  meta={"id": y, "desc": response.meta["desc"]})
            item["difficulty"] = i["difficulty"]
            item["rightRate"] = i["rightRate"]      # can be -1, if none.
            item["groupInfo"] = i["groupInfo"]      
            item["hot"] = i["hot"]                  # can be all 0, if none.
            item["questionAudio"] = i["questionAudio"]
            self.analysis(item)
            yield item
        qurl_list = question_url.split("page_num%3D")

        next_page_num = int(qurl_list[1]) + 1
        question_url = ''.join([qurl_list[0], "page_num%3D", str(next_page_num)])
        self.logger.info('Start crawling list {} page {}'.format(list_id, next_page_num) )
        yield Request(url = question_url, callback = self.parse_list, \
                      meta = {"list_id": list_id, "page_id": page_id, \
                              "subject": response.meta["subject"], "desc": response.meta["desc"]})

    # image sep., 
    # ?and wash out texts: html/body/span/ ?
    def process(self, text):
        soup = BeautifulSoup(text)
        imgs = soup.find_all("img")
        ans = []
        for i in imgs:
            if i["src"][0:7] == "http://":
                # print i["src"]
                temp = i["src"]
                i["src"] = str(uuid.uuid1())+'.'+i["src"][-3:]
                # print i["src"]
                ans += [(temp, i["src"])]
        return ans, str(soup)

    def storeImage(self, response):
        image = Image()
        img_id = response.meta["id"]
        desc = response.meta["desc"]
        descList = desc.split(">")
        img_dir = "images"
        for item in descList:
            img_dir += "/" + item.strip()
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
        image["url"] = img_id
        # print img_dir
        try:
            self.logger.info('Storing image now...')
            store_url = img_dir + "/" + img_id
            # print store_url
            f = open(store_url, 'wb')
            f.write(response.body)
            f.close()
            yield image
        except Exception, e:
            print e
            yield Request(url = response.url, callback = self.storeImage,  meta={"id": img_id})

    def semanticAnalysis(self, txt, item, c):
        tmpList = txt.split(u"A" + c)
        if len(tmpList) != 2:
            #Parse Failed
            return False
        tmpText = tmpList[1]
        tmpList = tmpText.split(u"B" + c)
        item['A'] = tmpList[0]
        if len(tmpList) != 2:
            #Parse Failed
            return False
        tmpText = tmpList[1]
        tmpList = tmpText.split(u"C" + c)
        item['B'] = tmpList[0]
        if len(tmpList) != 2:
            #Parse Failed
            return False
        tmpText = tmpList[1]
        tmpList = tmpText.split(u"D" + c)
        item['C'] = tmpList[0]
        if len(tmpList) != 2:
            #Parse Failed
            return False    
        item["D"] = tmpList[1]
        return True

    def analysis(self, item):
        # type: 0 => 选择题 1=>多选题 2 => 解答题 5=>完形填空题
        soup = BeautifulSoup(item["content"])
        colf43 = soup.find_all("span", class_="colf43")
        item["plainText"] = soup.text
        if len(colf43) != 0:
            item["source"] = colf43[0].text
        if item["questionType"] == "0":
            table = soup.find("table", attrs={"name": "optionsTable"})
            if table:
                tds = table.find_all("td")
                if len(tds) != 0:
                    # Normalized
                    item['A'] = tds[0].text[2:]
                    item['B'] = tds[1].text[2:]
                    item['C'] = tds[2].text[2:]
                    if len(tds) > 3:
                        item['D'] = tds[3].text[2:]
                    else:
                        # some of the choices have only A, B, C.
                        item['D'] = ''
            else:
                txt = re.sub(r"(?:<span.*?>|</span>|<p>|</p>|</body>|</html>|\n|\t)", '', soup.text)
                if self.semanticAnalysis(txt, item, u'.'):
                    return
                elif self.semanticAnalysis(txt, item, u')'):
                    return
                elif self.semanticAnalysis(txt, item, u'．'):
                    return
                

# command!, which can be paused and resumed.
# cd Document/Work/Cheese@SJTU/spider/zuoyehezi && scrapy crawl ZSpider -s JOBDIR=crawls/ZSpider-1
# use CTRL+C to pause.

# url = 
