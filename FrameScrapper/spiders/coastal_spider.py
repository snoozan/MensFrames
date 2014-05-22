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

class CoastalSpider(InitSpider):
    name = "coastal"
    allowed_domains=["http://www.coastal.com/"]
    start_urls = ["http://www.coastal.com/mens-frames?ilid=tnav#ui=cnd"]

    urls_list_xpath = '//*[@id="browsed-product"]/div[1]/div'
    item_fields = {'url': './@rel'}

    def __init__(self):
        InitSpider.__init__(self)
        self.verificationErrors = []
        self.selenium = webdriver.PhantomJS()

    def __del__(self):
        self.selenium.quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse(self, response):
        sel= self.selenium
        sel.get(response.url)
        sel.implicitly_wait(5)

        next = sel.find_element_by_xpath('//*[@id="pagination-nav-right"]')

        items = []
        sites = sel.find_elements_by_xpath('//*[@id="browsed-product"]/div[1]/div')

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.get_attribute("rel")
            items.append(item)

        while True:
            try:
                sel.implicitly_wait(10)
                print(sel.find_element_by_xpath('//*[@id="pagination-nav-right"]').get_attribute("onclick"))
                next.click()

                sites = sel.find_elements_by_xpath('//*[@id="browsed-product"]/div[1]/div')
                for site in sites:
                    item = FramescrapperItem()
                    item['url'] = site.get_attribute("rel")
                    items.append(item)

                next = sel.find_element_by_xpath('//*[@id="pagination-nav-right"]')

            except:
                print("I fail here " + sel.find_element_by_xpath('//*[@id="pagination-nav-right"]').get_attribute("onclick"))
                break

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
    """
