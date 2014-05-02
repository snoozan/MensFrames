from selenium import selenium

from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.http import Request

#from models import DBSession, framesInfo

from FrameScrapper.items import FramescrapperItem

class GlassesInfoSpider(Spider):
    name = "glassesinfo"

    #rules = ( Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_page',follow=True),         )

    allowed_domains=["http://www.glasses.com/"]
    start_urls=["http://www.glasses.com/women-glasses/ray-ban-rx5228-large/4595.html?dwvar_4595_color=tortoise2"]

    urls_list_xpath = '//*[@id="pdpMain"]'
    item_fields = {'url': '/html/head/link[5]/@href',
                   'brand': '//*[@id="brand-name"]/text()',
                   'product_name': '//*[@id="frame-name"]/text()',
                   'price': '//*[@id="frame-price"]/text()',
                   'colors': '//*[@id="color-selector-container"]/ul/li/a/title'
    }

    def __init__(self):
        Spider.__init__(self)
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://www.glasses.com/")
        self.selenium.start()

    def __del__(self):
        self.selenium.stop()
        print self.verificationErrors
        CrawlSpider.__del__(self)


    def parse(self, response):
        item = FramescrapperItem()

        hxs = HtmlXPathSelector(response)

        hxs.select('//*[@id="brand-name"]/text()').extract()

        sel = self.selenium
        try:
            sel.open(response.url)
        except:
            logging.error('ConnectionError, resting..')
            time.sleep(100)


        sel.get_text('//*[@id="brand-name"]/text()')
        yield item
    """
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
    """
