from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from FrameScrapper.items import FramescrapperItem

class LensCraftersSpider(Spider):
    name = "lenscrafters"
    allowed_domains=["http://www.glasses.com/"]
    start_urls=["http://www.glasses.com/men-glasses"]

    urls_list_xpath = '//*[@class="item"]'
    item_fields = {'url': './div[@class="names"]'
    }

    def parse(self, response):
        sel = HtmlXPathSelector(response)

        for site in sel.select(self.urls_list_xpath):
            loader = XPathItemLoader(FramescrapperItem(), selector=site)

            #define processes
            loader.dafault_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            for field, xpath in self.item_fields.iteritems():
                print(xpath)
                loader.add_xpath(field, xpath)
            yield loader.load_item()

