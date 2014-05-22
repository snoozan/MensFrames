# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter

class XmlExportPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('items.xml', 'a')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)

    def spider_closed(self, spider):
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        if spider.name not in ['eyeflyinfo', 'coastalinfo', 'mezzmerinfo', 'glassesinfo', 'thirtynineinfo', 'warbyparkerinfo', 'lenscraftersinfo', 'lookmaticinfo']:
            return item
        self.exporter.export_item(item)
        return item
