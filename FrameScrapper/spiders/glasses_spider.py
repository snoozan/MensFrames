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

class GlassesSpider(InitSpider):
    name = "glasses"
    allowed_domains=["http://www.glasses.com/"]
    start_urls=["http://www.glasses.com/men-glasses"]

    urls_list_xpath = '//div[@class="content slider"]/div[1]/a[@class="thumb-link"]'
    item_fields = {'url': './@href'
    }

    def __init__(self):
        InitSpider.__init__(self)
        self.verificationErrors = []
        self.selenium = webdriver.Firefox()

    def __del__(self):
        self.selenium.quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse(self, response):
        sel= self.selenium
        sel.get(response.url)
        sel.implicitly_wait(5)


        items = []
        sites = sel.find_elements_by_xpath(self.urls_list_xpath)



        next = sel.find_element_by_xpath('//*[@id="primary"]/div[2]/div[1]/div[1]/div[2]/ul/li[@class="first-last"]/a[@class="page-next"]')

        while True:
            try:


                print(sel.find_element_by_xpath('//*[@id="primary"]/div[2]/div[1]/div[1]/div[2]/ul/li[@class="current-page"]/span').text)
                print(sel.find_element_by_xpath('//*[@id="primary"]/div[2]/div[1]/div[1]/div[2]/ul/li[@class="first-last"]/a[@class="page-next"]').get_attribute("href"))

                sel.implicitly_wait(5)
                sites = sel.find_elements_by_xpath(self.urls_list_xpath)



                for site in sites:
                    item = FramescrapperItem()
                    item['url'] = site.get_attribute("href")
                    print(item['url'])
                    items.append(item)

                print("I'm clicking")
                next.click()

            except:
                break

        self.selenium.quit()
        return items
    """
    def parse(self, response):
        hxs = HtmlXPathSelector(response)


        for site in hxs.select(self.urls_list_xpath):
            loader = XPathItemLoader(FramescrapperItem(), selector=site)

            #define processes
            loader.dafault_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()


            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            yield loader.load_item()
        self.selenium.quit()
    """
