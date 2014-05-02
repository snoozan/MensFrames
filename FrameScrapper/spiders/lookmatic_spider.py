from scrapy.spider import Spider

from scrapy.selector import Selector
from FrameScrapper.items import FramescrapperItem

class LookmaticSpider(Spider):
    name = "lookmatic"
    allowed_domains = ["http://lookmatic.com/"]
    start_urls =[
        "http://lookmatic.com/collections/men",
            ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@id="wrapper-overall"]/div[@class="page-content-container"]/div[@class="page-collection"]/div[@id="collection-container"]/ul[@class="product-view"]/li[@class="hoverable"]')
        items = []
        for site in sites:
            item = FramescrapperItem()
            #item['url'] = site.xpath('./li/div[@class="prod-image-wrap"]/a/@href').extract()
            item['url'] = site.xpath('./a/@href').extract()
            items.append(item)
        print(items)
        print(sites.extract())
