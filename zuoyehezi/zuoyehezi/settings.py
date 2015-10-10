# -*- coding: utf-8 -*-

# Scrapy settings for zuoyehezi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zuoyehezi'

SPIDER_MODULES = ['zuoyehezi.spiders']
NEWSPIDER_MODULE = 'zuoyehezi.spiders'

ITEM_PIPELINES = ['zuoyehezi.pipelines.ZuoyeheziPipeline']

AUTOTHROTTLE_ENABLED = True

# LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 2

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zuoyehezi (+http://www.yourdomain.com)'
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'zuoyehezi.rotate_useragent.RotateUserAgentMiddleware' :400
    }