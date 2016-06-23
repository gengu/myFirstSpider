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
        # 这里是定义不同的爬虫起始点
        # 爬虫中，定义爬取入口很重要，针对买车达人这个网站，要爬取所有的车型就用第一个url
        'http://topka.cn/cars/brands'
        # 'http://topka.cn/cars/audi/q7'
        # 'http://topka.cn/cars/audi/q7/2016/26075'
    ]
    # 核心代码就这几行
    # 爬虫将爬取下来的页面中的url都抽取出来，那么我们针对不同的url返回做不同的处理
    def parse(self, response):
        p = re.compile(r'.*cars/brands$')
        p_cars = re.compile(r'http://topka.cn/cars/[\w\d]+/[\w\d]+$');
        p_car = re.compile(r'http://topka.cn/cars/[\w\d]+/[\w\d]+/[\d]+/[\d]+$')
        # 如果当前爬取的链接符合cars/brands 这个正则表达式
        if p.match(response.url):
            for sel in response.xpath('//ul/li'):
                if sel.xpath('a/@href') != '/':
                    # title = sel.xpath('a/text()').extract()
                    # 抽取出页面源码中的链接
                    link = sel.xpath('a/@href').extract()
                    item = BrandItems()
                    # item['title'] = title[0]
                    # 如果链接的个数大于0则继续处理
                    if(len(link) > 0):
                        # 组装一个类似于 http://topka.cn/cars/audi/q7的链接
                        item['link'] = str("http://topka.cn" + link[0])
                        if p_cars.match(item['link'].__str__()):
                            # 并且让scrapy爬虫核心系统去爬取这个页面，并且将回调方法设置成parse方法（也就是这个方法本身，可理解成递归）
                            req = Request(url=item['link'],callback=self.parse)
                            # yield如果你不明白的话，你就理解成，程序现在会把这个req返回给scrapy的核心爬取组件，然后scrapy会不断的请求parse方法
                            yield req
        # 如果当前url符合http://topka.cn/cars/audi/q7
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
                            # 同上，抽取链接 ，回调自己
                            req = Request(url = item['link'],callback=self.parse)
                            yield req
        # 这里表示的意思是终于找到了我们需要爬取的链接，例如：http://topka.cn/cars/audi/q7/2016/26075，那么我们要继续处理
        elif p_car.match(response.url):
            # 将其中的信息全部抽取出
            t_sel = response.xpath('//div[@id="j_carsmenu"]')
            brand = t_sel.xpath('//div[@id="j_fupinpai"]/*[@id="dLabel"]').xpath('@title').extract()[0].replace(' ','').replace('\n','')
            model = t_sel.xpath('//div[@id="j_fuchexi"]/*[@id="dLabel"]').xpath('text()').extract()[0].replace(' ','').replace('\n','');
            model_v = response.xpath('//h1[@class="car-name"]/text()').extract()[0]
            # 并且存储到CarItem中去
            item = CarItem()
            item['brand'] = brand
            item['model'] = model
            item['model_v'] = model_v
            p_sel = response.xpath('//div[@class="mod_pc param-configure-content"]')
            dict = {}
            # 详细的字段都抽取出来
            for sel1 in p_sel.xpath('ul[@class="mod_pc_ul"]/li'):
                if(len(sel1.xpath('p')[1].xpath('text()').extract()) > 0):
                    dict[sel1.xpath('p')[0].xpath('text()').extract()[0]] = sel1.xpath('p')[1].xpath('text()').extract()[0]
                else :
                    dict[sel1.xpath('p')[0].xpath('text()').extract()[0]] = ""
                item['value'] = dict
            # 和上面的yield不一样，这里返回的是一个item，那么scrapy获取到item了之后，会和上面的req有不同的处理方法
            # 这个定意思在settings.py的ITEM_PIPELINES字段，它定义了item该用什么方式去处理
            yield item
