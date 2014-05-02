from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

#from models import DBSession, framesInfo
from FrameScrapper.items import FramescrapperItem

class WarByParkerInfoSpider(Spider):
    name = "warbyparkerinfo"


    def __init__(self, url=None, *args, **kwargs):
        super(WarByParkerInfoSpider, self).__init__(*args, **kwargs)
        self.start_urls=[url]


    allowed_domains=["http://www.warbyparker.com/"]

    urls_list_xpath = '//*[@id="pdp"]/div[4]/div[1]'
    item_fields = {'url': '/html/head/link[1]/@href',
                   'brand': '//*[@id="js-product-purchase-section"]/div/h3[1]/text()',
                   'product_name': '//*[@id="js-product-purchase-section"]/div/h3[1]/text()',
                   'price': '//*[@id="js-product-purchase-section"]/div/p/span/span/text()',
                   'colors': '//*[@id="pdp"]/div[4]/div[1]/div[1]/div[2]/div[1]/ul/li/div/p/a/text()',
                   'width': '//*[@id="pdp"]/div[4]/div[1]/div[2]/ul[1]/li[1]/p/text()'
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
