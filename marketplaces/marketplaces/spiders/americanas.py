from loguru import logger as log
from datetime import datetime

import scrapy
# import os

from scrapy.exceptions import CloseSpider

from urllib.parse import urlparse
from uc_browser.browser_v2 import BrowserV2

from ..items import AmericanasItem


class AmericanasSpider(scrapy.Spider):
    name = 'americanas'
    allowed_domains = ['americanas.com.br']

    def __init__(self, search=None, filter=None, price=None, validate_freight=False, **kwargs):
        super().__init__(**kwargs)

        self.price = price
        self.freight = None
        self.validate_freight = validate_freight
        log.info(f'Validar frete: {self.validate_freight}')

        if search is None:
            raise CloseSpider('É necessário informar a palavra chave. Ex. -s "iphone"')

        self.keyword = search
        log.info(f'Palavra chave informada: {self.keyword}')

        # self.query_filter = '?filter={"id":"loja","value":"1p|Americanas|b2w.loja","fixed":false}&sortBy=relevance}'
        self.query_filter = '?filter=%7B"id"%3A"loja"%2C"value"%3A"1p%7CAmericanas%7Cb2w.loja"%2C"fixed"%3Afalse%7D&sortBy=relevance'

        # if filter is not None:
        #     self.query_filter = f'{self.query_filter}&{filter}'

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

        self.cookie_accept = '//*[contains(text(), "continuar e fechar")]'
        self.input_cep = '//span[@class="cep-placeholder"]'
        self.cep = '29160170'
        self.btn_ok_cep = '//button[contains(@class, "src__Button-sc-9")]'
        self.freight_field = '(//span[contains(@class, "freight-option-price")])[1]'
        self.cep_not_found = '//span[contains(text(), "Opa, CEP não encontrado")]'

    def start_requests(self):
        log.info('Acessando...')
        log.info(f'Pagina: {self.url}')
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        has_page = response.xpath(self.limit_page).get()
        if has_page:
            log.info('Não existem produtos nesta página.')
            raise CloseSpider('All page was scraped.')

        parsed_uri = urlparse(response.url)
        url_base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        cards = response.xpath(self.cards)
        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        for card in cards:
            item = AmericanasItem()
            item['created_at'] = str(today)
            item['product_name'] = card.xpath(self.product_name).get()
            item['product_price_sale'] = card.xpath(self.product_price_sale).get()
            item['product_url'] = url_base + card.xpath(self.product_url).get()

            if self.validate_freight:
                if self.freight is None:
                    self.set_freight(url=url_base + card.xpath(self.product_url).get())

            yield item

        self.offset += 24
        url = f'https://americanas.com.br/busca/{self.keyword}{self.query_filter}{self.query_offset.format(self.offset)}'
        log.info(f'Pagina: {url}')
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    def set_freight(self, url):
        log.info('Preparando para abrir o navegador.')
        try:
            web = BrowserV2(use_headless=True)
            web.navigate(url=url)
            log.info(f'Navegando na url: {url}')
            web.wait_to_click(xpath=self.cookie_accept, time=10)
            web.input_like_a_human(xpath=self.input_cep, send=self.cep)
            web.delay(start=2, end=4)
            web.click(xpath=self.btn_ok_cep)
            web.delay(start=5, end=8)

            if web.element_is_present(xpath=self.cep_not_found):
                log.warning(f'Cep não encontrado: {self.cep}')
            else:
                web.wait_element(xpath=self.freight_field)
                self.freight = web.get_text(xpath=self.freight_field)

            if self.freight is None:
                log.warning('O valor do frete não foi inserido.')
                self.freight = -1
            else:
                log.info('Valor do frete inserido com sucesso.')
                web.close_driver()

        except BaseException as err:
            log.error(f'Ocorreu um erro ao tentar acessar o navegador. {err}')


