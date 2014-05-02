from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from FrameScrapper.items import FramescrapperItem

class WarByParkerSpider(Spider):
    name = "warbyparker"
    allowed_domains=["http://www.warbyparker.com/"]
    start_urls = ["http://www.warbyparker.com/eyeglasses/men"]

    urls_list_xpath = '//ul[@class="products-grid"]/li/a'
    item_fields = {'url': './@href'}

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
