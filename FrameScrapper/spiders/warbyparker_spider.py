from selenium import selenium, webdriver

from scrapy.contrib.spiders.init import InitSpider
from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.http import Request

#from models import DBSession, framesInfo

from FrameScrapper.items import FramescrapperItem

class WarByParkerSpider(InitSpider):
    name = "warbyparker"
    allowed_domains=["http://www.warbyparker.com/"]
    start_urls = ["http://www.warbyparker.com/eyeglasses/men"]

    urls_list_xpath = '//*[@id="product_listing"]/li/div/a'
    item_fields = {'url': './@href'}

    def __init__(self):
        InitSpider.__init__(self)
        self.verificationErrors = []
        self.selenium = webdriver.PhantomJS()

    def __del__(self):
        self.selenium.quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    """
    def parse(self, response):
        sel = self.selenium
        sel.get(response.url)
        sel.implicitly_wait(10)

        sites = sel.find_elements_by_xpath('//*[@id="product_listing"]/li/div/a')
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.get_attribute("href")
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
