from selenium import selenium, webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from scrapy.contrib.spiders.init import InitSpider
from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.http import Request

import time
#from models import DBSession, framesInfo

from FrameScrapper.items import FramescrapperItem

class GlassesInfoSpider(Spider):
    name = "glassesinfo"


    def __init__(self,  *args, **kwargs):
        super(GlassesInfoSpider, self).__init__(**kwargs)

        self.verificationErrors = []
        #profile = webdriver.FirefoxProfile(profile_directory="/Applications/Firefox.app/Contents/MacOS")
        self.selenium = webdriver.PhantomJS()

        url = kwargs.get('url') or kwargs.get('domain')
        format(url.strip('"'))
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        urls = []
        urls.append(url)
        self.start_urls = urls

    rules = ( Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_page',follow=True),         )

    allowed_domains=["http://www.glasses.com/"]
    #start_urls=["http://www.glasses.com/women-glasses/ray-ban-rx5228-large/4595.html?dwvar_4595_color=black3"]

    urls_list_xpath = '//*[@id="pdpMain"]'
    item_fields = {'url': '/html/head/link[5]/@href',
                   'brand': '//*[@id="brand-name"]/text()',
                   'product_name': '//*[@id="frame-name"]/text()',
                   'price': '//*[@id="frame-price"]/text()',
                   'colors': '//*[@id="color-selector-container"]/ul/li/a/title'
    }
    def __del__(self):
        self.selenium.quit()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def wait_for_visibility(self, selector, the_xpath, timeout_seconds=10):
        retries = timeout_seconds
        while retries:
            print("TRYING FOR THE "+ str(retries) +"th TIME")
            try:
                elements = selector.find_elements_by_xpath(the_xpath)


                for element in elements:
                    if element.is_displayed():
                        print("the element is " + element.text)
                        return element

            except (NoSuchElementException, StaleElementReferenceException):
                if retries <= 0:
                    raise
                else:
                    pass

            retries = retries -1
            time.sleep(10)
        raise Exception("Element %s not visible despite waiting for %s seconds" (
        selector, timeout_seconds))


    def parse(self, response):

        sel = self.selenium
        sel.get(response.url)
        sel.implicitly_wait(10)
        sites = sel.find_elements_by_css_selector('#pdpMain > div.product-detail-wrap.product-image-container')
        print(sites)
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = response.url
            item['product_name'] = site.find_element_by_xpath('//*[@id="pdpMain"]/div[1]/div/div[1]/ol/li[4]/span').text



            colors = []
            for color in site.find_elements_by_xpath('//*[@id="color-selector-container"]/ul/li/a/div'):
                colors.append(color.get_attribute("class"))
            colorset = set()
            for color in colors:
                colorset.add(color)


            item['colors'] = list(colorset)

            item['price'] = site.find_element_by_css_selector('#frame-price').get_attribute("innerHTML")
            item['brand'] = site.find_element_by_xpath('//*[@id="pdpMain"]/div[1]/div/div[1]/ol/li[4]/span').text.split()[1]
            item['product_img'] = site.find_element_by_xpath('//*[@id="alternate-view-wrapper"]/li[1]/a').get_attribute("href")
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
    """
