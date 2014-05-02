
from scrapy.spider import Spider
from scrapy.selector import Selector

from FrameScrapper.items import FramescrapperItem

class WarByParkerSpider(Spider):
    name = "warbyparker"
    allowed_domains=["http://www.warbyparker.com/"]
    start_urls = ["http://www.warbyparker.com/eyeglasses/men"]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul[@class="products-grid"]/li/a')
        items = []

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.xpath('./@href').extract()
            items.append(item)
        return items
