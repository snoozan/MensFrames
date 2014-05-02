from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

#from models import DBSession, framesInfo
from FrameScrapper.items import FramescrapperItem

class ThirtyNineInfoSpider(Spider):
    name = "thirtynineinfo"


    def __init__(self, url=None, *args, **kwargs):
        super(ThirtyNineInfoSpider, self).__init__(*args, **kwargs)
        self.start_urls=[url]

    allowed_domains=["http://www.39dollarglasses.com/"]

    urls_list_xpath = '//*[@id="orderform"]/div'
    item_fields = {'url': '/html/head/link[@rel="canonical"]/@href',
                   'brand': '//*[@id="mid"]/div[1]/h1[1]/text()',
                   'product_name': '//*[@id="mid"]/div[1]/h1[1]/text()',
                   'price': '//*[@id="orderform"]/div/div[2]/div[1]/text()',
                   'colors': '//*[@id="orderform"]/div/div[1]/div[1]/div[@class="selectframe_colortext red_text"]/label/a/text()'
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
