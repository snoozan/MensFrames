 #Using Scrapy with Selenium to scape a rendered page [Updated]

from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.http import Request, FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from selenium import selenium, webdriver
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from FrameScrapper.items import FramescrapperItem

class LookmaticSpider(InitSpider):
    name = "lookmatic"
    allowed_domains = ["http://lookmatic.com/"]
    start_urls =[
        "http://lookmatic.com/collections/men",
            ]

    def __init__(self):
        InitSpider.__init__(self)
        self.verificationErrors = []
        self.selenium = webdriver.PhantomJS()

    def __del__(self):
        self.selenium.quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        sel = self.selenium
        sel.get(response.url)
        sel.implicitly_wait(10)
        sites = sel.find_elements_by_xpath('//*[@class="hoverable"]/div[@class="prod-image-wrap"]/a')
        print(sites)
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.get_attribute("href")
            items.append(item)
        return items
