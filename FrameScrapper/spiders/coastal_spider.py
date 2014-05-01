from scrapy.spider import Spider
from scrapy.selector import Selector

from FrameScrapper.items import FramescrapperItem

class CoastalSpider(Spider):
    name = "coastal"
    allowed_domains=["http://www.coastal.com/"]
    start_urls = ["http://www.coastal.com/mens-frames?ilid=tnav#ui=cnd"]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//*[@id="browsed-product"]/div[1]/div')
        items = []

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.xpath('./@rel').extract()
            items.append(item)
        return items
