
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

#from models import DBSession, framesInfo
from FrameScrapper.items import FramescrapperItem


class CoastalInfoSpider(Spider):
    name = "coastalinfo"



    def __init__(self, url=None, *args, **kwargs):
        super(CoastalInfoSpider, self).__init__(*args, **kwargs)
        self.start_urls=[url]



    allowed_domains=["http://www.coastal.com/"]
    start_urls=['http://www.coastal.com/r-hardy-9013-black?rsView=1&ga=M|F|K']

    urls_list_xpath = '//*[@id="product-content-right-container"]'
    item_fields = {'url': '/html/head/link[@rel="canonical"]/@href',
                   'brand': '//*[@id="product-brand-container"]/a/@href',
                   'product_name': '//*[@id="product-name-container"]/h1/text()',
                   'product_img': '//*[@id="product-main-image-container"]/a/@href',
                   'colors': '//*[@id="product-details-panes"]/div[1]/div/div[2]/ul/li[6]/span/text()',
                   'width': '//*[@id="product-details-panes"]/div[1]/div/div[3]/ul[3]/li[1]/text()',
                   'price': '//*[@id="price-amount"]/text()',
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
