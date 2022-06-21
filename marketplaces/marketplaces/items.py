# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DefaultItem(scrapy.Item):
    created_at = scrapy.Field()
    product_name = scrapy.Field()
    product_price_sale = scrapy.Field()
    product_url = scrapy.Field()
