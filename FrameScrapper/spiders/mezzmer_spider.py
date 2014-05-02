from scrapy.spider import Spider

from scrapy.selector import Selector
from FrameScrapper.items import FramescrapperItem

class MezzmerSpider(Spider):
    name = "mezzmer"
    allowed_domains = ["http://www.mezzmer.com"]
    start_urls =[
        "http://www.mezzmer.com/mens/mens-optical",
            ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//*[@id="galleria"]/ul[@class="product_content"]/li/figure/a')
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.xpath('./@href').extract()
            items.append(item)
        return items
