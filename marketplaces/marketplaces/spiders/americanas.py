from loguru import logger as log

import scrapy
# import os

from scrapy.exceptions import CloseSpider

from urllib.parse import urlparse

from ..items import AmericanasItem


class AmericanasSpider(scrapy.Spider):
    name = 'americanas'
    allowed_domains = ['americanas.com.br']

    def __init__(self, search=None, filter=None, price=None, **kwargs):
        super().__init__(**kwargs)

        if search is None:
            raise CloseSpider('É necessário informar a palavra chave. Ex. -s "iphone"')

        self.keyword = search
        log.info(f'Palavra chave informada: {self.keyword}')

        self.query_filter = '?filter={"id":"loja","value":"1p|Americanas|b2w.loja","fixed":false}&sortBy=relevance}'
        if filter is not None:
            self.query_filter = f'{self.query_filter}&{filter}'

        log.info(f'Filtro configurado: {self.query_filter}')

        self.query_offset = '&limit=24&offset={}'
        self.offset = 0
        # self.path_output = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', '{}'))

        self.url = f'https://americanas.com.br/busca/{self.keyword}{self.query_filter}{self.query_offset.format(self.offset)}'

        self.cards = '//*[contains(@class, "ColGridItem")]'
        self.product_url = './/a/@href'
        self.product_name = './/*[contains(@class, "product-name")]/text()'
        self.product_price_sale = './/*[contains(@class, "PromotionalPrice")]/text()'
        self.limit_page = '//*[contains(text(), "poxa, nenhum resultado encontrado para ")]'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        log.info('Acessando...')
        log.info(f'Pagina: {self.url}')
        has_page = response.xpath(self.limit_page).get()
        if has_page:
            log.info('Não existem produtos nesta página.')
            raise CloseSpider('All page was scraped.')

        parsed_uri = urlparse(response.url)
        url_base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        cards = response.xpath(self.cards)
        for card in cards:
            item = AmericanasItem()
            item['product_name'] = card.xpath(self.product_name).get()
            item['product_price_sale'] = card.xpath(self.product_price_sale).get()
            item['product_url'] = url_base + card.xpath(self.product_url).get()

            yield item

        self.offset += 24
        yield scrapy.Request(
            url=f'https://americanas.com.br/busca/{self.keyword}{self.query_filter}{self.query_offset.format(self.offset)}',
            callback=self.parse
        )
