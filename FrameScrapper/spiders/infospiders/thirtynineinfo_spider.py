from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

#from models import DBSession, framesInfo
from FrameScrapper.items import FramescrapperItem

class ThirtyNineInfoSpider(Spider):
    name = "thirtynineinfo"


    def __init__(self,  **kwargs):
        super(ThirtyNineInfoSpider, self).__init__(**kwargs)
        url = kwargs.get('url') or kwargs.get('domain')
        format(url.strip('"'))
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        urls = []
        urls.append(url)
        self.start_urls = urls

    allowed_domains=["http://www.39dollarglasses.com/"]

    urls_list_xpath = '//*[@id="orderform"]/div'
    item_fields = {'url': '/html/head/link[@rel="canonical"]/@href',
                   'brand': '//*[@id="mid"]/div[1]/h1[1]/text()',
                   'product_name': '//*[@id="mid"]/div[1]/h1[1]/text()',
                   'product_img': '//*[@id="frame_tab1"]/div/div[1]/img[1]/@src',
                   'width': '//*[@id="orderform"]/div/div[3]/div[1]/div[1]/div[1]/span[1]/text()',
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
