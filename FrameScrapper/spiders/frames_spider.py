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
        sites = sel.xpath('//div[@class="product_box"]/div')
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['brand'] = site.xpath('//h5/a/text()').extract()
            item['url'] = site.xpath('//h5/a/@href').extract()
            item['colors'] = site.xpath('//div[@class="available_colors"]//img/text()').extract()
            item['price'] = site.xpath('//div[@class="product_bprice"]/text()').extract()
            item['retail_price']= site.xpath('//div[@class="product_btext"]/text()').extract()
            items.append(item)
        return items


