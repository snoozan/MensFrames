from scrapy.spider import Spider

from scrapy.selector import Selector
from FrameScrapper.items import FramescrapperItem

class ThirtyNineSpider(Spider):
    name = "thirtynine"
    allowed_domains = ["http://www.39dollarglasses.com"]
    start_urls =[
            "http://www.39dollarglasses.com/mens-eyeglasses.html",
            ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="product_box"]')
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.xpath('.//a[@class="order_now"]/@href').extract()
            items.append(item)
        return items
