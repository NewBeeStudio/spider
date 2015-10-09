#-*- coding:utf-8 -*-
from scrapy.spider import Spider
from scrapy import Request
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit 
from bs4.element import NavigableString 
from zuoyehezi.items import ZItem
from zuoyehezi.items import Image
from scrapy.http import FormRequest
import urlparse
import json
import urllib
import uuid

interface_url = "/Interface.aspx?url=" # seems to be interface btw front/back-end.
assignment_url = "/Assignment.aspx?url="
login_suffix = "@php/v1_user/teacher/login?source=webTeahcer&version=2.4.0"
main_url = "http://www.zuoyehezi.com"

def getSubject(subject):
    subjects = {"0": u"数学", "1":u"语文", "2":u"英语","3": u"物理", "4":u"化学", "5":u"生物", "6":u"历史", "7":u"地理", "8":u"政治"}
    return subjects[subject]

class ZSpider(Spider):
    name = "ZSpider"
    start_urls = []
    start_urls = start_urls + ["http://www.zuoyehezi.com"]

    def parse(self, response):
        cookiename = 'GkLJW7sRsxtg6zKEK4bQWApwflkAGRZQOSzsoODaKy5AJmbR0Vt+pCfg+i51FwSz' # cookie: knowbox_teacherToken.
        ID = '1478'              # id for question list.
        questionType =  '-1'    # -1: all, 0: choice, 1:multi-choice, 2: answer, 5: cloze.
        collectType =   '0'     # undefined / 0 / 1, function unknown.
        outType =       '2'     # undefined / 0 / 2, function unknown.
        pagesize =      '10'    # questions per page
        pagenum =       '0'     # pagination num.
        tmp_url =   "@php/v1_tiku/knowledge/question?source=webTeacher&from=kb&token=%s&version=2.4.0&knowledge_id=%s&question_type=%s&collect=%s&out=%s&page_size=%s&page_num=%s" % \
                    (cookiename, ID, questionType, collectType, outType, pagesize, pagenum)

        question_url = main_url + interface_url + urllib.quote(tmp_url, safe='')
        yield Request(url = question_url, callback=self.analysis)

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

    def analysis(self, response):
        q_l = json.loads(response.body)["data"]["list"]
        for i in q_l:
            item = ZItem()
            item["questionType"] = i["questionType"]
            item["questionID"] = i["questionID"]
            item["questionNo"] = i["questionNo"]
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
            item["rightRate"] = i["rightRate"]
            item["groupInfo"] = i["groupInfo"]
            item["hot"] = i["hot"]
            item["questionAudio"] = i["questionAudio"]
            yield item


    # def store(self, response):
    #     f = open("temp.html", "w")
    #     f.write(response.body)
    #     f.close()

'''
    def parse(self, response):
        yield Request(url="http://www.zuoyehezi.com/Interface.aspx?url=%40php%2Fv1_user%2Fteacher%2Flogin%3Fsource%3DwebTeahcer%26version%3D2.4.0", callback=self.parse_next, \
                method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"}, \
                body="mobile=13122262056&password=password123")
    def parse_next(self, response):
        print response.body
        data = json.loads(response.body)
        data = data["data"]

        self.cookie = u"knowbox_teacherToken=" + data["token"] + u";"
        self.cookie += u"knowbox_teacherInfo="
        self.cookie += data["userID"] + u"|"
        self.cookie += data["userName"] + u"|"
        self.cookie += data["headPhoto"] + u"|"
        self.cookie += getSubject(data["subject"]) + u"|"
        self.cookie += data["schoolName"] + u"|"
        #self.cookie += data["regDate"] + u"|"
        self.cookie += u"undefined|"
        self.cookie += data["gradePart"] + u"|"
        self.cookie += data["mobile"] + u";"
        self.cookie += u"knowbox_teacherClassList=" + json.dumps(data["classList"]) + u";"

        yield Request(url = "http://www.zuoyehezi.com/Assignment.aspx",  \
                headers = {"Cookie": self.cookie}, \
                callback = self.store)
'''
