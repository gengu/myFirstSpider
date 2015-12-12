__author__ = 'genxiaogu'

from scrapy.item import Item, Field
class CarsItem(Item):
    title = Field()
    desc = Field()
    link = Field()
    brand = Field()
    model = Field()

