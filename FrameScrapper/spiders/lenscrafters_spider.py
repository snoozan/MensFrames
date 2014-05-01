
from scrapy.spider import Spider
from scrapy.selector import Selector

from FrameScrapper.items import FramescrapperItem

class LensCrafterSpider(Spider):
    name = "lenscrafters"
    allowed_domains=["http://www.lenscrafters.com/"]
    start_urls = ["http://www.lenscrafters.com/lc-us/mens-eyeglasses"]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="item_container"]/div[@class="item"]')
        items = []

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.xpath('./div[@class="container"]/div[@class="names"]/a/@href').extract()
            items.append(item)
        return items
