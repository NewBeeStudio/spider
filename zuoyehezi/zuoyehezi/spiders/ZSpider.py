#-*- coding:utf-8 -*-
from scrapy.spider import Spider
from scrapy import Request
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit 
from bs4.element import NavigableString 
from zuoyehezi.items import ZItem
from scrapy.http import FormRequest
import urlparse
import json

def getSubject(subject):
    subjects = {"0": u"数学", "1":u"语文", "2":u"英语","3": u"物理", "4":u"化学", "5":u"生物", "6":u"历史", "7":u"地理", "8":u"政治"}
    return subjects[subject]

class GalaxyTsingHua(Spider):
    name = "ZSpider"
    start_urls = []
    start_urls = start_urls + ["http://www.zuoyehezi.com"]

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

    def store(self, response):
        f = open("temp.html", "w")
        f.write(response.body)
        f.close()