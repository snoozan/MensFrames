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

class GlassesInfoSpider(Spider):
    name = "glassesinfo"


    def __init__(self,  *args, **kwargs):
        super(GlassesInfoSpider, self).__init__(**kwargs)

        self.verificationErrors = []
        profile = webdriver.FirefoxProfile(profile_directory="/Applications/Firefox.app/Contents/MacOS")
        self.selenium = webdriver.Firefox(profile)

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

    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        sel = self.selenium
        sel.get(response.url)
        sel.implicitly_wait(10)
        sites = sel.find_elements_by_xpath('//*[@id="pdpMain"]')
        print(sites)
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = site.find_element_by_xpath('/html/head/link[5]').get_attribute("href")
            item['brand'] = site.find_element_by_xpath('//*[@id="product-content-wrapper"]/div[1]/div[1]/h1/span[1]').text
            item['product_name'] = site.find_element_by_xpath('//*[@id="product-content-wrapper"]/div[1]/div[1]/h1/span[2]').text
            item['price'] = site.find_element_by_xpath('//*[@id="product-content-wrapper"]/div[1]/div[2]/span').text
            colors = []
            for color in site.find_elements_by_xpath('//*[@id="thumbnails"]/ul/li[2]/div/div/div/ul/li[@class="thumb with-label"]/a'):
                colors.append(color.get_attribute("data-color"))
            item['colors'] = colors
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
