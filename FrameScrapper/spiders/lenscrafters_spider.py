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

class LensCraftersSpider(InitSpider):
    name = 'lenscrafters'
    allowed_domains = ['linkedin.com']
    start_urls = ["http://www.lenscrafters.com/lc-us/mens-eyeglasses"]

    urls_list_xpath ='//*[@id="product_list_container"]/div[2]/div[@class="item_container"]/div/div[1]/div[@class="names"]/a'
    item_fields = {'url': './@href'}

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

        next = sel.find_element_by_xpath('//*[@id="WC_CategoryOnlyResultsDisplay_links_2"]')
        print(next.get_attribute("href"))

        items = []
        sites = sel.find_elements_by_xpath('//div[@class="item_container"]/div/div[@class="container"]/div[@class="names"]/a')

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.get_attribute("href")
            items.append(item)

        while True:
            try:
                next.click()

                sel.implicitly_wait(5)
                sites = sel.find_elements_by_xpath('//*[@id="product_list_container"]/div[2]/div[@class="item_container"]/div/div[1]/div[@class="names"]/a')

                for site in sites:
                    item = FramescrapperItem()
                    item['url'] = site.get_attribute("href")
                    items.append(item)

                next = sel.find_element_by_xpath('//*[@id="WC_CategoryOnlyResultsDisplay_links_2"]')

            except:
                break

        self.selenium.quit()
        return items










        """
        try:

            sites = sel.find_elements_by_xpath('//*[@id="product_list_container"]/div[2]/div[@class="item_container"]/div/div[1]/div[@class="names"]/a')

            for site in sites:
                item = FramescrapperItem()
                item['url'] = site.get_attribute("href")
                items.append(item)

        except:
            break
        hxs = HtmlXPathSelector(response)

        for site in hxs.select(self.urls_list_xpath):
            loader = XPathItemLoader(FramescrapperItem(), selector=site)

            #define processes
            loader.dafault_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            yield loader.load_item()

        hxs = HtmlXPathSelector(response)
        sel = self.selenium
        sel.get(response.url)
        sel.implicitly_wait(10)
        sites = hxs.select('//*[@id="product_list_container"]/div[2]/div[@class="item_container"]/div/div[1]/div[@class="names"]/a')
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.select('./@href').extract()
            items.append(item)
        return items
        """
