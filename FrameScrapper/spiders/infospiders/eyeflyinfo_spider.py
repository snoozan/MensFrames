
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
class EyeFlyInfoSpider(Spider):
    name = "eyeflyinfo"


    def __init__(self, **kwargs):
        super(EyeFlyInfoSpider, self).__init__(**kwargs)

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

    allowed_domains=["http://www.eyefly.com/"]

    urls_list_xpath = '//*[@id="body-wrapper"]/div/div[4]/div'
    item_fields = {
                   'url': '//*[@id="pdp-list-prd-like"]/div[1]/@onclick',
                   'brand': '//*[@id="pdp-title"]/h1/text()',
                   'product_name': '//*[@id="pdp-title"]/h1/text()',
                   'product_img': '//*[@id="carrousel-1210-wrapper"]/ul/li[1]/div/div[3]/img/@src',
                   'width': '//*[@id="pdp-motion-description"]/text()[4]',
                   'price': '//*[@id="pdp-add-to-cart-prd-price"]/*[@id="pdp-price-block"]/text()',
                   'colors': '//*[@id="body-prd-colors"]/a/@href',
    }


    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        sel = self.selenium
        sel.get(response.url)
        sel.implicitly_wait(10)
        sites = sel.find_elements_by_xpath('//*[@id="body-wrapper"]/div/div[4]/div')
        print(sites)
        items = []
        for site in sites:
            item = FramescrapperItem()
            item['url'] = self.start_urls[0]
            item['brand'] = "Eyefly"
            item['product_name'] = site.find_element_by_xpath('/html/head/meta[8]').get_attribute("content")
            item['price'] = site.find_element_by_xpath('//*[@id="pdp-add-to-cart-prd-price"]/*[@id="pdp-price-block"]').text
            colors = []
            for color in site.find_elements_by_xpath('//*[@id="body-prd-colors"]/a/div'):
                colors.append(color.get_attribute("id"))
            item['colors'] = colors
            item['product_img'] = site.find_element_by_xpath('//div[@class="wrapper"]/ul/li[1]/div/div[3]/img').get_attribute("src")
            items.append(item)

        self.selenium.quit()
        return items
