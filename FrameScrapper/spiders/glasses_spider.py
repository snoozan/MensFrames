from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.http import Request, FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector, Selector

from selenium import selenium, webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

import urlparse

from FrameScrapper.items import FramescrapperItem

class GlassesSpider(InitSpider):
    name = "glasses"
    allowed_domains=["www.glasses.com/"]
    start_urls=["http://www.glasses.com/men-glasses"]

    urls_list_xpath = '//div[@class="content slider"]/div[1]/a[@class="thumb-link"]'
    item_fields = {'url': './@href'
    }

    def __init__(self):
        InitSpider.__init__(self)
        self.verificationErrors = []

    def __del__(self):
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//*[@id="primary"]/div[2]/div[1]/div[1]/div[2]/ul/li/a/@href').extract()
        urls.append(response.url)
        urls = set(urls)
        print(urls)
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


    """
    def parse(self, response):
        sel= self.selenium
        sel.get(response.url)
        sel.implicitly_wait(5)


        items = []

        sites = sel.find_elements_by_xpath(self.urls_list_xpath)



        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.get_attribute("href")
            print(item['url'])
            items.append(item)


        next = sel.find_element_by_xpath('//*[@id="primary"]/div[2]/div[1]/div[1]/div[2]/ul/li[@class="first-last"]/a[@class="page-next"]')

        while True:
            try:


                print("I am on page "+  sel.find_element_by_xpath('//*[@id="primary"]/div[2]/div[1]/div[1]/div[2]/ul/li[@class="current-page"]/span').text)

                sel.implicitly_wait(5)
                sel.get(next.get_attribute("href"))
                sites = sel.find_elements_by_xpath(self.urls_list_xpath)



                for site in sites:
                    item = FramescrapperItem()
                    item['url'] = site.get_attribute("href")
                    print(item['url'])
                    items.append(item)

                print("I'm clicking this link "+sel.find_element_by_xpath('//*[@id="primary"]/div[2]/div[1]/div[1]/div[2]/ul/li[@class="first-last"]/a[@class="page-next"]').get_attribute("href"))
                next.click()


                next = sel.find_element_by_xpath('//*[@id="primary"]/div[2]/div[1]/div[1]/div[2]/ul/li[@class="first-last"]/a[@class="page-next"]')
            except:


                print("I fail here "+sel.find_element_by_xpath('//*[@id="primary"]/div[2]/div[1]/div[1]/div[2]/ul/li[@class="first-last"]/a[@class="page-next"]').get_attribute("href"))
                break

        self.selenium.quit()
        return items
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
