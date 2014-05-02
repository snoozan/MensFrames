
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from models import DBSession, framesInfo

from FrameScrapper.items import FramescrapperItem

class MezzmerSpider(Spider):
    name = "mezzmerinfo"
    allowed_domains=["http://www.mezzmer.com/"]
    start_urls=[""]

    urls_list_xpath = ''
    item_fields = {'url': '',
                   'brand': '',
                   'product_name': '',
                   'price': '',
                   'color': ''
    }

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
