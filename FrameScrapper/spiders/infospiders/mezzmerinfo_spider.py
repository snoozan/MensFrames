
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

class MezzmerSpider(Spider):
    name = "mezzmerinfo"


    def __init__(self, **kwargs):
        super(MezzmerSpider, self).__init__(**kwargs)


        self.verificationErrors = []
        self.selenium = webdriver.PhantomJS()

        url = kwargs.get('url') or kwargs.get('domain')
        format(url.strip('"'))
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        urls = []
        urls.append(url)
        self.start_urls = urls

    rules = ( Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_page',follow=True),         )

    allowed_domains=["http://www.mezzmer.com/"]
    urls_list_xpath = '//*[@id="container"]/div[2]'
    item_fields = {'url': '/html/head/link[9]/@href',
                   'brand': '//*[@id="container"]/div[2]/div[2]/div[1]/aside/h1/text()',
                   'product_name': '//*[@id="container"]/div[2]/div[2]/div[1]/aside/h1/text()',
                   'price': '//*[@id="container"]/div[2]/div[2]/div[1]/aside/h1/div/span/text()',
                   'colors': '//*[@id="container"]/div[2]/div[2]/div[2]/div/div/ul/li/h3/text()'
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
        sites = sel.find_elements_by_xpath('//*[@id="container"]/div[2]')
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = self.start_urls[0]
            item['brand'] = site.find_element_by_xpath('/html/body/header/div[1]/a').get_attribute('href')
            item['product_name'] = site.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/div[1]/aside/h1').text
            item['price'] = site.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/div[1]/aside/h1/div/span').text
            colors = []
            for color in site.find_elements_by_xpath('//*[@id="container"]/div[2]/div[2]/div[2]/div/div/ul/li/h3'):
                colors.append(color.text)
            item['colors'] = colors
            item['product_img'] = site.find_element_by_xpath('//*[@id="MagicToolboxSelectorsContainer"]/div/div/ul/li[1]/a/img').get_attribute("src")
            item['width'] = site.find_element_by_xpath('//*[@id="container"]/div[2]/article[1]/aside/div[1]/dl/dd[1]/strong').text
            items.append(item)

        self.selenium.quit()
        return items
