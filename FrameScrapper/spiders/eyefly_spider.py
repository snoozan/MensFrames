from scrapy.spider import Spider
from scrapy.selector import Selector

from FrameScrapper.items import FramescrapperItem

class EyeFlySpider(Spider):
    name = "eyefly"
    allowed_domains = ["http://www.eyefly.com/"]
    start_urls = ['http://www.eyefly.com/men/shop-men/eyeglasses.html']

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="category-products"]/ul/li/div[2]/h2/a')
        items = []

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.xpath('./@href').extract()
            items.append(item)
        return items
