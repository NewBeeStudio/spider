#-*- coding: utf-8 -*-

import scrapy
import mysql.connector
import time
from zuoyehezi.items import ZItem
from zuoyehezi.items import Image

user = 'root'
password = ''
database = 'ZYHZ1'

class DBHandler(object):
    def __init__(self):
        self.cnx = self.db_connect()
        self.cursor = self.cnx.cursor()

    def db_connect(self):
        cnx = mysql.connector.connect(user = user, password = password, host = '127.0.0.1', database = database)
        return cnx

    def insert(self, item, source_date = None):
        if isinstance(item, ZItem):
            add_news = ("INSERT INTO QUESTION "
                  "(`subject`, `type`, `id`, `no`, `description`, `content`, `rightAnswer`, `answerExplain`, `difficulty`, `rightRate`, `hot`, `A`, `B`, `C`, `D`, `source`, `plainText`) "
                  "VALUES (%(subject)s ,%(type)s, %(id)s, %(no)s, %(description)s, %(content)s, %(rightAnswer)s, %(answerExplain)s, %(difficulty)s, %(rightRate)s, %(hot)s, %(A)s, %(B)s, %(C)s, %(D)s, %(source)s, %(plainText)s)")

            data_news = {
                'subject' : item["subject"],
                'type' : item["questionType"],
                'id' : item["questionID"],        
                'no' : item["questionNo"],
                'description': item["description"],        
                'content' : item["content"],        
                'rightAnswer' :  item["rightAnswer"],        
                'answerExplain' : item["answerExplain"],    
                'difficulty' : item["difficulty"],
                'rightRate' : item["rightRate"],
                'hot' : item["hot"],
                'storeTime': time.strftime('%Y-%m-%d'),
                'A': item.get('A', ''),
                'B': item.get('B', ''),
                'C': item.get('C', ''),
                'D': item.get('D', ''),
                'source': item.get('source', ''),
                'plainText': item.get('plainText', ''),
            }
            
            try:
                self.cursor.execute(add_news, data_news)
                self.cnx.commit()
            except:
                raise
        elif isinstance(item, Image):
            add_news = ("INSERT INTO IMAGE_URL "
                  "(`url`) "
                  "VALUES (%(url)s)")
            data_news = {
                "url" : str(item["url"]),
            }

            try:
                self.cursor.execute(add_news, data_news)
                self.cnx.commit()
            except:
                raise
