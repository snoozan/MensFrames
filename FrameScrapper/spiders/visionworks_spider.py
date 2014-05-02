
from scrapy.spider import Spider
from scrapy.selector import Selector

from FrameScrapper.items import FramescrapperItem

class VisionWorksSpider(Spider):
    name = "visionworks"
    allowed_domains=["http://www.visionworks.com/"]
    start_urls = ["http://www.visionworks.com/men/index.php"]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@id="frames_nav"]')
        items = []

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.xpath('./@href').extract()
            items.append(item)
        print(sites.extract())
        return items
