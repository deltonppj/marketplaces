# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DefaultItem(scrapy.Item):
    loja_nome = scrapy.Field()
    created_at = scrapy.Field()
    product_sku = scrapy.Field()
    product_name = scrapy.Field()
    product_price_sale = scrapy.Field()
    product_url = scrapy.Field()


class ShopSmilesItem(DefaultItem):
    product_gain_miles = scrapy.Field()


class RedeemItem(DefaultItem):
    product_reedem = scrapy.Field()

