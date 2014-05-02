from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from FrameScrapper.items import FramescrapperItem

class ClassicSpecsSpider(Spider):
    name = "classicspecs"
    allowed_domains = ["http://www.classicspecs.com/"]
    start_urls=["http://www.classicspecs.com/collections/mens-collection-summer-2011"]

    urls_list_xpath = '//*[@id="collection-main"]/div/div[1]/ul'
    item_fields = {'url': './/li/a[1]/@href'}

    def parse(self, response):
        sel = HtmlXPathSelector(response)

        for site in sel.select(self.urls_list_xpath):
            loader = XPathItemLoader(FramescrapperItem(), selector=site)

            #define processes
            loader.dafault_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            yield loader.load_item()
