
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
#from models import DBSession, framesInfo

from FrameScrapper.items import FramescrapperItem

class EyeFlyInfoSpider(Spider):
    name = "eyeflyinfo"


    def __init__(self, **kwargs):
        super(EyeFlyInfoSpider, self).__init__(**kwargs)
        url = kwargs.get('url') or kwargs.get('domain')
        format(url.strip('"'))
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        urls = []
        urls.append(url)
        self.start_urls = urls



    allowed_domains=["http://www.eyefly.com/"]

    urls_list_xpath = '//*[@id="body-wrapper"]/div/div[4]/div'
    item_fields = {
                   'url': '//*[@id="pdp-list-prd-like"]/div[1]/@onclick',
                   'brand': '//*[@id="pdp-title"]/h1/text()',
                   'product_name': '//*[@id="pdp-title"]/h1/text()',
                   'product_img': '//*[@id="carrousel-1210-wrapper"]/ul/li[1]/div/div[3]/img/@src',
                   'width': '//*[@id="pdp-motion-description"]/text()[4]',
                   'price': '//*[@id="pdp-add-to-cart-prd-price"]/*[@id="pdp-price-block"]/text()',
                   'colors': '//*[@id="body-prd-colors"]/a/@href',
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
