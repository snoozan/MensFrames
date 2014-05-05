
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

        for site in hxs.select(self.urls_list_xpath):
            loader = XPathItemLoader(FramescrapperItem(), selector=site)

            #define processes
            loader.dafault_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            yield loader.load_item()

        self.selenium.quit()
