# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from zuoyehezi.db_handler import DBHandler

class ZuoyeheziPipeline(object):
  def __init__(self):
    self.db = DBHandler()
  def process_item(self, item, spider):
    self.db.insert(item)
    return item
