from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from FrameScrapper.items import FramescrapperItem

class CoastalSpider(Spider):
    name = "coastal"
    allowed_domains=["http://www.coastal.com/"]
    start_urls = ["http://www.coastal.com/mens-frames?ilid=tnav#ui=cnd"]

    urls_list_xpath = '//*[@id="browsed-product"]/div[1]/div'
    item_fields = {'url': './@rel'}


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
