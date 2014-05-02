# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class FramescrapperItem(Item):
    # define the fields for your item here like:

    url = Field()
    brand = Field()
    product_name = Field()
    product_img = Field()
    colors = Field()
    width = Field()
    price = Field()

