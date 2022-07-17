# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProgramasPontoItem(scrapy.Item):
    loja_nome = scrapy.Field()
    nome = scrapy.Field()
    valor_bonus = scrapy.Field()
    valor_bonus_parcial = scrapy.Field()
    valor_real = scrapy.Field()

