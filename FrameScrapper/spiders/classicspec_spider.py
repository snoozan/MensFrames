from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from FrameScrapper.items import FramescrapperItem

class ClassicSpecsSpider(Spider):
    name = "classicspecs"
    allowed_domains = ["http://www.classicspecs.com/"]
    start_urls=["http://www.classicspecs.com/collections/mens-collection-summer-2011"]

    def parse(self, response):
        if 'news.ycombinator.com' in response.url:

            hxs = HtmlXPathSelector(response)
            sites = hxs.selector('//*[@id="collection-main"]/div/div[1]/ul')
            items = []
            for site in sites:
                item = FramescrapperItem()
                item['url'] = site.select('.//li/a[1]/@href').extract()

                items.append(item)
            return items
