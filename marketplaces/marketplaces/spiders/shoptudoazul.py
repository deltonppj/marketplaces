from loguru import logger as log
from datetime import datetime

import scrapy
import os

from scrapy.exceptions import CloseSpider

from urllib.parse import urlparse
from uc_browser.browser_v2 import BrowserV2

from ..items import RedeemItem


class ShoptudoazulSpider(scrapy.Spider):
    name = 'shoptudoazul'
    custom_settings = {'ITEM_PIPELINES': {'marketplaces.pipelines.ReedemPipeline': 300}}

    def __init__(self, search=None, filter=None, price=None, validate_freight=False, **kwargs):
        super().__init__(**kwargs)
        log.info(f'Crawler iniciado: {self.name}')
        self.price = price
        log.info(f'Preço desejado: {self.price}')
        self.freight = None
        self.validate_freight = validate_freight
        log.info(f'Validar frete: {self.validate_freight}')

        if search is None:
            raise CloseSpider('É necessário informar a palavra chave. Ex. -s "iphone"')

        self.keyword = search
        log.info(f'Palavra chave informada: {self.keyword}')

        self.page = 1
        self.url = f'https://shopping.tudoazul.com/categoria/{self.page}?q={self.keyword}&hs=true'

        self.cards = '//div[contains(@class, "standard")]'
        self.product_url = './a/@href'
        self.product_name = './/h3[contains(@class, "productName")]/text()'
        self.product_reedem = './/span[@class="promo-label-small"]/following-sibling::span/text()'
        self.limit_page = 9

    def start_requests(self):
        log.info('Acessando...')
        log.info(f'Pagina: {self.url}')
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        if self.page > self.limit_page:
            log.info('Não existem produtos nesta página.')
            raise CloseSpider('All page was scraped.')

        parsed_uri = urlparse(response.url)
        url_base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        cards = response.xpath(self.cards)
        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        for card in cards:

            product_sku = card.xpath(self.product_url).get().split('/')[3]

            item = RedeemItem()
            item['created_at'] = str(today)
            item['product_sku'] = product_sku
            item['product_name'] = card.xpath(self.product_name).get()
            item['product_reedem'] = card.xpath(self.product_reedem).get()
            item['product_url'] = url_base + card.xpath(self.product_url).get()

            yield item

        self.page += 1
        url = f'https://shopping.tudoazul.com/categoria/{self.page}?q={self.keyword}&hs=true'
        log.info(f'Pagina: {url}')
        yield scrapy.Request(url=url, callback=self.parse)


