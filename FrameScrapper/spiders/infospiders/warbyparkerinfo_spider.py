from selenium import selenium, webdriver

from scrapy.contrib.spiders.init import InitSpider

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request

from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

#from models import DBSession, framesInfo
from FrameScrapper.items import FramescrapperItem

class WarByParkerInfoSpider(Spider):
    name = "warbyparkerinfo"


    def __init__(self, **kwargs):
        super(WarByParkerInfoSpider, self).__init__(**kwargs)

        self.verificationErrors = []
        self.selenium = webdriver.PhantomJS()

        url = kwargs.get('url') or kwargs.get('domain')
        format(url.strip('"'))
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://www.warbyparker.com%s' % url
        urls = []
        urls.append(url)
        self.start_urls = urls

    rules = ( Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_page',follow=True),         )


    urls_list_xpath = '//*[@id="pdp"]/div[4]/div[1]'
    item_fields = {'url': '/html/head/link[1]/@href',
                   'brand': '//*[@id="header"]/div/div[1]/div/strong/text()',
                   'product_name': '//*[@id="js-product-purchase-section"]/div/h3[1]/text()',
                   'product_img': '//*[@id="pdp"]/div[4]/div[1]/div[1]/div[1]/div/div[1]/div/img/@src',
                   'price': '//*[@id="js-product-purchase-section"]/div/p/span/span/text()',
                   'colors': '//*[@id="pdp"]/div[4]/div[1]/div[1]/div[2]/div[1]/ul/li/div/p/a/text()',
                   'width': '//*[@id="pdp"]/div[4]/div[1]/div[2]/ul[1]/li[1]/p/text()'
    }

    def __del__(self):
        self.selenium.quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse(self, response):

        print("I'm doing things")
        sel = self.selenium
        sel.get(response.url)
        sel.implicitly_wait(10)
        sites = sel.find_elements_by_xpath('//*[@id="pdp"]/div[@class="product-optical"]')
        print sites
        items = []

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.find_element_by_xpath('/html/head/link[1]').get_attribute("href")
            item['brand'] = sel.find_element_by_xpath('//*[@id="top-nav-logo"]/img').get_attribute("alt")
            item['product_name'] = site.find_element_by_xpath('//*[@id="js-product-purchase-section"]/div/h3[1]').text
            item['price'] = site.find_element_by_xpath('//*[@id="js-product-purchase-section"]/div/p/span/span').text
            colors = []
            for color in site.find_elements_by_xpath('//*[@id="pdp"]/div[4]/div[1]/div[1]/div[2]/div[1]/ul/li/div/p/a'):
                colors.append(color.text)
            item['colors'] = colors
            item['product_img'] = site.find_element_by_xpath('//*[@id="pdp"]/div[4]/div[1]/div[1]/div[1]/div/div[1]/div/img').get_attribute("src")
            item['width'] = site.find_element_by_xpath('//*[@id="pdp"]/div[4]/div[1]/div[2]/ul[1]/li[1]/p').text
            items.append(item)

        self.selenium.quit()
        return items
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

        self.selenium.quit()
    """


