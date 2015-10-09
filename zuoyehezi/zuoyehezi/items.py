# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ZItem(scrapy.Item):
    questionType = scrapy.Field()
    questionID = scrapy.Field()
    questionNo = scrapy.Field()
    content = scrapy.Field()
    rightAnswer = scrapy.Field()
    answerExplain = scrapy.Field()
    difficulty = scrapy.Field()
    rightRate = scrapy.Field()
    groupInfo = scrapy.Field()
    hot = scrapy.Field()
    questionAudio = scrapy.Field()

class Image(scrapy.Item):
    id = scrapy.Field()
    data = scrapy.Field()