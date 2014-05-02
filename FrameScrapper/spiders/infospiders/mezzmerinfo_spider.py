
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
#from models import DBSession, framesInfo

from FrameScrapper.items import FramescrapperItem

class MezzmerSpider(Spider):
    name = "mezzmerinfo"
    allowed_domains=["http://www.mezzmer.com/"]
    start_urls=["http://www.mezzmer.com/big-easy-eyewear-black-fade-eyeglass-frame"]

    urls_list_xpath = '//*[@id="container"]/div[2]'
    item_fields = {'url': '/html/head/link[9]/@href',
                   'brand': '//*[@id="container"]/div[2]/div[2]/div[1]/aside/h1/text()',
                   'product_name': '//*[@id="container"]/div[2]/div[2]/div[1]/aside/h1/text()',
                   'price': '//*[@id="container"]/div[2]/div[2]/div[1]/aside/h1/div/span/text()',
                   'colors': '//*[@id="container"]/div[2]/div[2]/div[2]/div/div/ul/li/h3/text()'
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
