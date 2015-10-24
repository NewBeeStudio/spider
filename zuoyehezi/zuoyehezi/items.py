# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ZItem(scrapy.Item):
    subject = scrapy.Field()
    questionType = scrapy.Field()
    questionID = scrapy.Field()
    questionNo = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    rightAnswer = scrapy.Field()
    answerExplain = scrapy.Field()
    difficulty = scrapy.Field()
    rightRate = scrapy.Field()
    groupInfo = scrapy.Field()
    hot = scrapy.Field()
    questionAudio = scrapy.Field()
    A = scrapy.Field()
    B = scrapy.Field()
    C = scrapy.Field()
    D = scrapy.Field()
    plainText = scrapy.Field()
    source = scrapy.Field()

class Image(scrapy.Item):
    url = scrapy.Field()

# class Url_crawled(scrapy.Item):
#     id = scrapy.Field()
#     list_id = scrapy.Field()
#     page_id = scrapy.Field()