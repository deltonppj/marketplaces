# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmericanasItem(scrapy.Item):
    product_name = scrapy.Field()
    product_price_sale = scrapy.Field()
    product_url = scrapy.Field()
