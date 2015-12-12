import scrapy
import re
import json

from myfirstspider.items import BrandItems
from myfirstspider.CarsItem import CarsItem
from myfirstspider.CarItem import CarItem
from scrapy.http import Request
from scrapy.utils.url import urljoin_rfc

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["topka.cn"]
    start_urls = [
        'http://topka.cn/cars/brands'
        # 'http://topka.cn/cars/audi/q7'
        # 'http://topka.cn/cars/audi/q7/2016/26075'
    ]
    def parse(self, response):
        p = re.compile(r'.*cars/brands$')
        p_cars = re.compile(r'http://topka.cn/cars/[\w\d]+/[\w\d]+$');
        p_car = re.compile(r'http://topka.cn/cars/[\w\d]+/[\w\d]+/[\d]+/[\d]+$')
        if p.match(response.url):
            for sel in response.xpath('//ul/li'):
                if sel.xpath('a/@href') != '/':
                    # title = sel.xpath('a/text()').extract()
                    link = sel.xpath('a/@href').extract()
                    item = BrandItems()
                    # item['title'] = title[0]
                    if(len(link) > 0):
                        item['link'] = str("http://topka.cn" + link[0])
                        if p_cars.match(item['link'].__str__()):
                            req = Request(url=item['link'],callback=self.parse)
                            yield req
        elif p_cars.match(response.url):
            t_sel = response.xpath('//*[@id="dLabel"]')
            title = t_sel[1].xpath('text()').extract()[1].replace(' ','')
            brand_sel = response.xpath('//button[@id="dLabel"]')
            brand = brand_sel[0].xpath('@title').extract()
            for sel in response.xpath('//tbody/tr/td/a'):
                if sel.xpath('@href') != '/':
                    link = sel.xpath('@href').extract();
                    item = CarsItem()
                    item['title'] = title[0]
                    item['brand'] = brand[0]
                    if(len(link) > 0):
                        item['link'] = str("http://topka.cn" + link[0])
                        if p_car.match(item['link'].__str__()):
                            req = Request(url = item['link'],callback=self.parse)
                            yield req
        elif p_car.match(response.url):
            t_sel = response.xpath('//div[@id="j_carsmenu"]')
            brand = t_sel.xpath('//div[@id="j_fupinpai"]/*[@id="dLabel"]').xpath('@title').extract()[0].replace(' ','').replace('\n','')
            model = t_sel.xpath('//div[@id="j_fuchexi"]/*[@id="dLabel"]').xpath('text()').extract()[0].replace(' ','').replace('\n','');
            model_v = response.xpath('//h1[@class="car-name"]/text()').extract()[0]
            item = CarItem()
            item['brand'] = brand
            item['model'] = model
            item['model_v'] = model_v
            p_sel = response.xpath('//div[@class="mod_pc param-configure-content"]')
            dict = {}
            for sel1 in p_sel.xpath('ul[@class="mod_pc_ul"]/li'):
                if(len(sel1.xpath('p')[1].xpath('text()').extract()) > 0):
                    dict[sel1.xpath('p')[0].xpath('text()').extract()[0]] = sel1.xpath('p')[1].xpath('text()').extract()[0]
                else :
                    dict[sel1.xpath('p')[0].xpath('text()').extract()[0]] = ""
                item['value'] = dict
            yield item





