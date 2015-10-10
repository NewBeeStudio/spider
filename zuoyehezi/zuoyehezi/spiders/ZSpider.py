#-*- coding:utf-8 -*-
from scrapy.spider import Spider
from scrapy import Request, log
from scrapy.http import FormRequest
from zuoyehezi.items import ZItem
from zuoyehezi.items import Image
from bs4 import BeautifulSoup, UnicodeDammit
from bs4.element import NavigableString
import urlparse
import json
import urllib
import uuid


# Initialization.
interface_url = "/Interface.aspx?url=" # seems to be interface btw front/back-end.
assignment_url = "/Assignment.aspx?url="
login_suffix = "@php/v1_user/teacher/login?source=webTeahcer&version=2.4.0"
main_url = "http://www.zuoyehezi.com"

# get the idx range of every subject. only English currently.
def getRange(idx):
    # "0": u"数学", "1":u"语文", "2":u"英语","3": u"物理", "4":u"化学", "5":u"生物", "6":u"历史", "7":u"地理", "8":u"政治"
    startIdx = [0, 0, 206, 0, 0, 0, 0, 0, 0]
    lastIdx = [0, 0, 311, 0, 0, 0, 0, 0, 0]
    return startIdx[idx], lastIdx[idx]

class ZSpider(Spider):
    name = "ZSpider"
    start_urls = []
    start_urls = start_urls + ["http://www.zuoyehezi.com"]


    def parse(self, response):

        cookiename = 'GkLJW7sRsxtg6zKEK4bQWApwflkAGRZQOSzsoODaKy5AJmbR0Vt+pCfg+i51FwSz' # cookie: knowbox_teacherToken.
        ID = 0                  # id for question list.
        questionType =  '-1'    # -1: all, 0: choice, 1:multi-choice, 2: answer, 5: cloze.
        collectType =   '0'     # undefined / 0 / 1, function unknown.
        outType =       '0'     # undefined / 0 / 2, function unknown.
        pagesize =      '10'    # questions per page
        pagenum =       '0'     # pagination num.    
        
        # every subject:
        for subject in range(9):
            start, end = getRange(subject)
            if start == 0 and end == 0:
                continue

            start = 200
            end = 200
            for ID in range(start, end+1):
                tmp_url = "@php/v1_tiku/knowledge/question?source=webTeacher&from=kb&token=%s&version=2.4.0&knowledge_id=%s&question_type=%s&collect=%s&out=%s&page_size=%s&page_num=%s" % \
                          (cookiename, ID, questionType, collectType, outType, pagesize, pagenum)
                
                question_url = main_url + interface_url + urllib.quote(tmp_url, safe='')
                # analysis and store
                yield Request(url = question_url, callback = self.parse_list, meta = {"subject": subject})

    def parse_list(self, response):

        totalPageNum = json.loads(response.body)["data"]["totalPageNum"]
        print totalPageNum
        self.analysis(response)
        for pagenum in range(1, totalPageNum):
            # derive url for next page using split/join.
            question_url = ''.join([response.url.split("page_num")[0], "page_num%3D", str(pagenum)])
            # question_url = "http://www.zuoyehezi.com/Interface.aspx?url=%40php%2Fv1_tiku%2Fknowledge%2Fquestion%3Fsource%3DwebTeacher%26from%3Dkb%26token%3D1HUuLSP7HSqJ4NyK1I0qMTHHr7Rxmz2bVJ3FRYFrO%2FOS6YF8mmNsqNbreKvmqebU%26version%3D2.4.0%26knowledge_id%3D211%26question_type%3D0%26collect%3D0%26out%3D0%26page_size%3D10%26page_num%3D0"
            yield Request(url = question_url, callback = self.analysis, meta = {"subject": response.meta["subject"]})

    # image sep., 
    # ?and wash out texts: html/body/span/ ?
    def process(self, text):
        soup = BeautifulSoup(text)
        imgs = soup.find_all("img")
        ans = []
        for i in imgs:
            if i["src"][0:7] == "http://":
                temp = i["src"]
                i["src"] = uuid.uuid1()
                ans += [(temp, i["src"])]
        return ans, str(soup)

    def analysis(self, response):
        print "HERE"
        data = json.loads(response.body)
        if data["code"] != "99999":
            self.logger.warning('PageInfo: No data exists or Forbiden')
            return
        q_l = data["data"]["list"]
        # print "******"
        # print q_l
        # print "******"
        for i in q_l:
            item = ZItem()
            item["subject"] = response.meta["subject"]
            item["questionType"] = i["questionType"]
            item["questionID"] = i["questionID"]
            item["questionNo"] = i["questionNo"]
            # process: in case of images. same below.
            temp, item["content"] = self.process(i["content"])
            for x, y in temp:
                yield Request(url = x, callback = self.storeImage,  meta={"id": y})
            temp, item["rightAnswer"] = self.process(i["rightAnswer"])
            for x, y in temp:
                yield Request(url = x, callback = self.storeImage,  meta={"id": y})
            temp, item["answerExplain"] = self.process(i["answerExplain"])
            for x, y in temp:
                yield Request(url = x, callback = self.storeImage,  meta={"id": y})
            item["difficulty"] = i["difficulty"]
            item["rightRate"] = i["rightRate"]      # can be -1, if none.
            item["groupInfo"] = i["groupInfo"]      
            item["hot"] = i["hot"]                  # can be all 0, if none.
            item["questionAudio"] = i["questionAudio"]
            yield item

    def storeImage(self, response):
        image = Image()
        image["id"] = response.meta["id"]
        image["data"] = response.body
        yield image
