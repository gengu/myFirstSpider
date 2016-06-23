# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class MyfirstspiderPipeline(object):
    def __init__(self):
        self.file = open('aba.txt','wb')

    def process_item(self, item, spider):
        if item:
            line = json.dumps(dict(item)) + "\n"
            print line
            # 这里将一行文件写入本地文件
            self.file.write(line.decode('unicode_escape'))
            # item['brand'] = item['brand'][0].decode('UTF-8')
            # self.file.write(dict(item).__str__() + "\n");
        return item
