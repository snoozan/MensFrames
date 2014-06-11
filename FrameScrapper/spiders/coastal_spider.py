 #Using Scrapy with Selenium to scape a rendered page [Updated]

from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.http import Request, FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from selenium import selenium, webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

import urlparse

from FrameScrapper.items import FramescrapperItem
import time

class CoastalSpider(InitSpider):
    name = "coastal"
    allowed_domains=["http://www.coastal.com/"]
    start_urls = ["http://www.coastal.com/mens-frames?ilid=tnav#ui=cnd"]

    urls_list_xpath = '//*[@id="browsed-product"]/div[1]/div'
    item_fields = {'url': './@rel'}

    def __init__(self):
        InitSpider.__init__(self)
        self.verificationErrors = []

    def __del__(self):
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse(self, response):
        urls = []
        i = 1
        while i < 46:
            urls.append('http://www.coastal.com/mens-frames?ilid=tnav#attr_searchGenders=[Men]&minPrice=0&maxPrice=500&sorting=featuredAnywhere-asc&page=%s&searchFamily=glasses&categoryCode=MaleFrames&filterGroup=&pdi_=[]&widgetExpanded=false&perfectFitExpanded=false&requestIdentifier=16139&hotSpotsEnabled=true&order=[searchGenders_Men]' % i)
            i+=1
        for url in urls:
            url = urlparse.urljoin(response.url, url)
            self.log('Found item link: %s' %url)
            yield Request(url, callback=self.parseGlasses, dont_filter=True)

    def parseGlasses(self, response):
        sel = HtmlXPathSelector(response)

        for site in sel.select(self.urls_list_xpath):
            loader = XPathItemLoader(FramescrapperItem(), selector=site)

            #define processes
            loader.dafault_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            yield loader.load_item()

