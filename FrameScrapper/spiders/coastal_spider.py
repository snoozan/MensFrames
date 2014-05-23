 #Using Scrapy with Selenium to scape a rendered page [Updated]

from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.http import Request, FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from selenium import selenium, webdriver
from selenium.common.exceptions import NoSuchElementException
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

    def wait_for_visibility(self, xpath_path, timeout_seconds=10):
        retries = timeout_seconds
        while retries:
            print("TRYING FOR THE "+ retries +"th TIME")
            try:
                print("I'm running")
                element = self.selenium.find_element_by_xpath('//*[@id="pagination-nav-right"]').get_attribute("onclick")
                if element.is_displayed():
                    return element

            except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                if retries <= 0:
                    raise
                else:
                    pass

            retries = retries -1
            time.sleep(10)
        raise self.ElementNotVisibleException("Element %s not visible despite waiting for %s seconds" (
        xpath_path, timeout_seconds))



    def parse(self, response):
        sel= self.selenium
        sel.get(response.url)
        sel.implicitly_wait(5)

        next =  sel.find_element_by_xpath('//*[@id="pagination-nav-right"]')

        items = []
        sites = sel.find_elements_by_xpath('//*[@id="browsed-product"]/div[1]/div')

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.get_attribute("rel")
            items.append(item)

        while True:
            try:
                sel.implicitly_wait(10)
                print("clicking")
                next.click()


                next = sel.find_element_by_xpath('//*[@id="pagination-nav-right"]')

                sites = sel.find_elements_by_xpath('//*[@id="browsed-product"]/div[1]/div')
                for site in sites:
                    item = FramescrapperItem()
                    item['url'] = site.get_attribute("rel")
                    items.append(item)

            except:
                print("I fail here " + sel.find_element_by_xpath('//*[@id="pagination-nav-right"]').get_attribute("onclick"))
                break

        return items
        self.selenium.quit()
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
