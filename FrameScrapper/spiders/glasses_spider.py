from scrapy.spider import Spider
from scrapy.selector import Selector

from FrameScrapper.items import FramescrapperItem

class GlassesSpider(Spider):
    name = "glasses"
    allowed_domains=["http://www.glasses.com/"]
    start_urls=["http://www.glasses.com/men-glasses"]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="content slider"]/div[1]/a')
        items = []

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.xpath('./@href').extract()
            items.append(item)
        return items
