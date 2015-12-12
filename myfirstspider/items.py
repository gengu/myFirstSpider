# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


# 品牌主页 可以获取每一个车型
class BrandItems(Item):
    title = Field()
    desc = Field()
    link = Field()




