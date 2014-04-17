from scrapy.spider import Spider

from scrapy.selector import Selector
from FrameScrapper.items import FramescrapperItem

class FrameSpider(Spider):
    name = "frames"
    allowed_domains = ["http://www.39dollarglasses.com"]
    start_urls =[
            "http://www.39dollarglasses.com/mens-eyeglasses.html",
            ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="product_box"]')
        for site in sites:
            color = sel.xpath('//div[@class="product_btext"]').extract()
            price = sel.xpath('//div[@class="product_bprice"]').extract()

