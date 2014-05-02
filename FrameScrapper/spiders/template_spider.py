
from scrapy.spider import Spider
from scrapy.selector import Selector

from FrameScrapper.items import FramescrapperItem

class Template(Spider):
    name = ""
    allowed_domains=[""]
    start_urls = [""]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('')
        items = []

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.xpath('.').extract()
            items.append(item)
        return items
