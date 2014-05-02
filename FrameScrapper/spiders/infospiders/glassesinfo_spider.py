
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
#from models import DBSession, framesInfo

from FrameScrapper.items import FramescrapperItem

class GlassesInfoSpider(Spider):
    name = "glassesinfo"
    allowed_domains=["http://www.glasses.com/"]
    start_urls=["http://www.glasses.com/women-glasses/ray-ban-rx5228-large/4595.html?dwvar_4595_color=tortoise2"]

    urls_list_xpath = '//*[@id="pdpMain"]'
    item_fields = {'url': '/html/head/link[5]/@href',
                   'brand': '//*[@id="brand-name"]/text()',
                   'product_name': '//*[@id="frame-name"]/text()',
                   'price': '//*[@id="frame-price"]/text()',
                   'colors': '//*[@id="color-selector-container"]/ul/li/a/title'
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
