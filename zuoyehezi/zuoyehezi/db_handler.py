#-*- coding: utf-8 -*-

import scrapy
import mysql.connector
import time
from zuoyehezi.items import ZItem
from zuoyehezi.items import Image

user = 'root'
password = ''

class DBHandler(object):
    def __init__(self):
        self.cnx = self.db_connect()
        self.cursor = self.cnx.cursor()

    def db_connect(self):
        cnx = mysql.connector.connect(user = user, password = password, host = '127.0.0.1', database = 'ZYHZ')
        return cnx

    def insert(self, item, source_date = None):
        if isinstance(item, ZItem):
            add_news = ("INSERT INTO QUESTION "
                  "(`subject`, `type`, `id`, `no`, `content`, `rightAnswer`, `answerExplain`, `difficulty`, `rightRate`, `hot`) "
                  "VALUES (%(subject)s ,%(type)s, %(id)s, %(no)s, %(content)s, %(rightAnswer)s, %(answerExplain)s, %(difficulty)s, %(rightRate)s, %(hot)s)")

            data_news = {
                'subject' : item["subject"],
                'type' : item["questionType"],
                'id' : item["questionID"],        
                'no' : item["questionNo"],        
                'content' : item["content"],        
                'rightAnswer' :  item["rightAnswer"],        
                'answerExplain' : item["answerExplain"],    
                'difficulty' : item["difficulty"],
                'rightRate' : item["rightRate"],
                'hot' : item["hot"],
                'storeTime': time.strftime('%Y-%m-%d')
            }
            
            try:
                self.cursor.execute(add_news, data_news)
                self.cnx.commit()
            except:
                raise
        elif isinstance(item, Image):
            add_news = ("INSERT INTO IMAGE "
                  "(`id`, `data`) "
                  "VALUES (%(id)s, %(data)s)")
            data_news = {
                "id" : str(item["id"]),
                "data": item["data"],
                "storeTime": time.strftime('%Y-%m-%d')
            }

            try:
                self.cursor.execute(add_news, data_news)
                self.cnx.commit()
            except:
                raise
        # elif isinstance(item, Url_crawled):
        #     add_news = ("INSERT INTO URL_CRAWLED "
        #           "(`id`, `list_id`, `page_id`) "
        #           "VALUES (%(id)s, %(list_id)s, %(page_id)s)")
        #     data_news = {
        #         "id" : item["id"],
        #         "list_id": item["list_id"],
        #         "page_id": item["page_id"],
        #     }

        #     try:
        #         self.cursor.execute(add_news, data_news)
        #         self.cnx.commit()
        #     except:
        #         raise
