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

class ThirtyNineSpider(InitSpider):
    name = "thirtynine"
    allowed_domains = ["http://www.39dollarglasses.com"]
    start_urls =[
            "http://www.39dollarglasses.com/mens-eyeglasses.html",
            ]
    urls_list_xpath = '//div[@class="product_box"]/a[@class="order_now"]'
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


        items = []
        sites = sel.find_elements_by_xpath(self.urls_list_xpath)

        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.get_attribute("href")
            items.append(item)

        while True:
            try:
                nextbuttons = sel.find_elements_by_xpath('//*[@id="mid"]/div[3]/div[4]/form/ul/li/a')

                for nextbutton in nextbuttons:
                    if 'Next' in nextbutton.text:
                        print("The next page is "+ nextbutton.text)
                        next = nextbutton
                    else:
                        print("This is button " + nextbutton.text)


                next.click()

                sites = sel.find_elements_by_xpath(self.urls_list_xpath)

                print("I'm on page number "+ sel.find_element_by_xpath('//a[@class="active notLink"]').text)


                for site in sites:
                    item = FramescrapperItem()
                    item['url'] = site.get_attribute("href")
                    print(item['url'])
                    items.append(item)


            except:
                print("I fail here " + sel.find_element_by_xpath('//a[@class="active notLink"]').text)
                break

        self.selenium.quit()
        return items


