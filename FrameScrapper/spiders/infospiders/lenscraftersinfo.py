

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

class LensCraftersInfoSpider(Spider):
    name = "lenscraftersinfo"


    def __init__(self, **kwargs):
        super(LensCraftersInfoSpider, self).__init__(**kwargs)


        self.verificationErrors = []
        self.selenium = webdriver.PhantomJS()

        url = kwargs.get('url') or kwargs.get('domain')
        format(url.strip('"'))
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        urls = []
        urls.append(url)
        self.start_urls = urls

    rules = ( Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_page',follow=True),         )

    allowed_domains=["http://www.lenscrafters.com/"]



    def __del__(self):
        self.selenium.quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse(self, response):
        sel = self.selenium
        sel.get(response.url)
        sel.implicitly_wait(10)
        sites = sel.find_elements_by_xpath('//*[@id="main_content_wrapper"]')
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = self.start_urls[0]
            item['brand'] = site.find_element_by_xpath('//*[@id="catalog_link"]').text
            item['product_name'] = site.find_element_by_xpath('//*[@id="catalog_link"]').text
            item['price'] = site.find_element_by_xpath('//*[@id="price"]').text
            item['colors'] = site.find_element_by_xpath('//*[@id="WC_CachedItemDisplay_div_15"]/div[2]/ul/li[1]').text
            item['product_img'] = site.find_element_by_xpath('//*[@id="productMainImage"]').get_attribute("src")
            items.append(item)

        self.selenium.quit()
        return items
