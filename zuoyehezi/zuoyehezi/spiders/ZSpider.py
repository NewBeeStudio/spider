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
import re, time, random


# Initialization.
interface_url = "/Interface.aspx?url=" # seems to be interface btw front/back-end.
assignment_url = "/Assignment.aspx?url="
login_suffix = "@php/v1_user/teacher/login?source=webTeahcer&version=2.4.0"
main_url = "http://www.zuoyehezi.com"
cookienameList = [
                  '1HUuLSP7HSqJ4NyK1I0qMTHHr7Rxmz2bVJ3FRYFrO%2FOS6YF8mmNsqNbreKvmqebU',
                  'GkLJW7sRsxtg6zKEK4bQWApwflkAGRZQOSzsoODaKy5AJmbR0Vt+pCfg+i51FwSz',
                 ]

# get the idx range of every subject. only English currently.
def getRange(idx):
    # "0": u"英语", "1":u"语文", "2":u"数学","3": u"物理", "4":u"化学", "5":u"生物", "6":u"历史", "7":u"地理", "8":u"政治"
    startIdx = [206, 0, 3, 0, 0, 0, 0, 0, 0]
    lastIdx = [311, 0, 205, 0, 0, 0, 0, 0, 0]
    return startIdx[idx], lastIdx[idx]

class ZSpider(Spider):
    name = "ZSpider"
    start_urls = []
    start_urls = start_urls + ["http://www.zuoyehezi.com"]

    def parse(self, response):

        cookiename = cookienameList[1] # cookie: knowbox_teacherToken.
        ID = 0                  # id for question list.
        questionType =  '-1'    # -1: all, 0: choice, 1:multi-choice, 2: answer, 5: cloze.
        collectType =   '0'     # undefined / 0 / 1, function unknown.
        outType =       '0'     # undefined / 0 / 2, function unknown.
        pagesize =      '10'    # questions per page
        pagenum =       '0'     # pagination    num.    
        
        # every subject:
        for subject in range(9):
            start, end = getRange(subject)
            if start == 0 and end == 0:
                continue

            # start = 220
            for ID in range(start, end+1):
                tmp_url = "@php/v1_tiku/knowledge/question?source=webTeacher&from=kb&token=%s&version=2.4.0&knowledge_id=%s&question_type=%s&collect=%s&out=%s&page_size=%s&page_num=%s" % \
                          (cookiename, ID, questionType, collectType, outType, pagesize, pagenum)
                
                question_url = main_url + interface_url + urllib.quote(tmp_url, safe='')
                # analysis and store
                self.download_delay = 20
                self.logger.info('Start crawling list %d page 0', ID)
                yield Request(url = question_url, callback = self.parse_list, \
                              meta = {"list_id": ID, "page_id": 0, "subject": subject})

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
            # gap = float("%.2f" % random.uniform(2, 4))
            # time.sleep(gap)
            self.download_delay = 20
            self.logger.info("Oops! Crawler going too fast!")
            # qList = question_url.split("%26")
            # qList[2] = "token%3D" + random.choice(cookienameList)
            # question_url = "%26".join(qList)
            yield Request(question_url, callback = self.parse_list, \
                          meta = {"list_id": list_id, "page_id": page_id, "subject": response.meta["subject"]})
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
        qurl_list = question_url.split("page_num%3D")

        next_page_num = int(qurl_list[1]) + 1
        question_url = ''.join([qurl_list[0], "page_num%3D", str(next_page_num)])
        self.logger.info('Start crawling list {} page {}'.format(list_id, next_page_num) )
        yield Request(url = question_url, callback = self.parse_list, \
                      meta = {"list_id": list_id, "page_id": page_id, "subject": response.meta["subject"]})

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

    def storeImage(self, response):
        image = Image()
        image["id"] = response.meta["id"]
        image["data"] = response.body
        yield image

# command!, which can be paused and resumed.
# cd Document/Work/Cheese@SJTU/spider/zuoyehezi && scrapy crawl ZSpider -s JOBDIR=crawls/ZSpider-1
# use CTRL+C to pause.

# url = 
