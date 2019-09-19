# -*- coding: utf-8 -*-

#引入文件

import scrapy

class UserItem(scrapy.Item):
# 标签
    name = scrapy.Field()
    sex = scrapy.Field()
    privince = scrapy.Field()
    # city = scrapy.Field()
    job = scrapy.Field()
    time = scrapy.Field()
    projects= scrapy.Field()

