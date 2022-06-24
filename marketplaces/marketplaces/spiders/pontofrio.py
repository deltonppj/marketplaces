import time

from loguru import logger as log
from datetime import datetime
import json

import scrapy
# import os

from scrapy.exceptions import CloseSpider

from urllib.parse import urlparse
from uc_browser.browser_v2 import BrowserV2

from ..items import DefaultItem


class PontofrioSpider(scrapy.Spider):
    name = 'pontofrio'

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

        self.index = 1
        self.filter = 'd%3A1186322%3A1186324'  # Vendido pela loja
        self.query_filter = f'?resultsPerPage=20&terms={self.keyword}&filter={self.filter}&page={self.index}&salesChannel=desktop&apiKey=pontofrio'

        if filter is not None:
            self.filter = filter
        log.info(f'Filtro configurado: {self.query_filter}')

        self.url = f'https://prd-api-partner.viavarejo.com.br/api/search{self.query_filter}'
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }

        self.input_cep = '//input[@id="frete"]'
        self.cep = '29160170'
        self.btn_ok_cep = '//button[@aria-label="Consultar frete"]'
        self.freight_field = '(//span[contains(@class, "cep-item--value")])[1]'
        self.freight_error = '//p[contains(@class, "cep-error")]'

    def start_requests(self):
        log.info('Acessando...')
        log.info(f'Pagina: {self.index} - {self.url}')
        yield scrapy.Request(url=self.url,
                             method='GET',
                             headers=self.headers,
                             callback=self.parse)

    def parse(self, response, **kwargs):
        current_nav = 0  # Controle webdriver
        try_again = 3
        data = json.loads(response.text)
        products = data.get('products')
        log.debug(f'Produtos encontrados: {len(products)}')

        next_pagination = data.get('pagination')['next']

        for product in products:
            is_available = product['status']

            if is_available == 'AVAILABLE':
                product_sku = product['skus'][0]['sku']
                product_item = {
                    'name': product['name'],
                    'url': product['url']
                }

                if current_nav <= try_again:
                    if self.validate_freight:
                        if (self.freight is None) | (self.freight == -1):
                            self.set_freight(url=product['url'])
                    current_nav += 1

                url = f'https://pdp-api.pontofrio.com.br/api/v2/sku/{product_sku}/price/source/PF?utm_source=undefined&take=undefined&device_type=MOBILE'
                yield scrapy.Request(
                    url=url,
                    method='GET',
                    headers=self.headers,
                    callback=self.parse_price,
                    cb_kwargs={'product_item': product_item})

        if next_pagination:
            self.index += 1
            url = f'https://prd-api-partner.viavarejo.com.br/api/search?resultsPerPage=20&terms={self.keyword}&filter={self.filter}&page={self.index}&salesChannel=desktop&apiKey=pontofrio'
            log.info(f'Pagina: {self.index} - {url}')
            yield scrapy.Request(
                url=url,
                method='GET',
                headers=self.headers,
                callback=self.parse)

    def parse_price(self, response, product_item):
        data = json.loads(response.text)
        price = data['paymentMethodDiscount']['sellPriceWithDiscount']

        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        item = DefaultItem()
        item['created_at'] = str(today)
        item['product_sku'] = product_item['url'].split('=')[1]
        item['product_name'] = product_item['name']
        item['product_price_sale'] = price
        item['product_url'] = product_item['url']

        yield item

    def set_freight(self, url):
        web = None
        log.info('Preparando para abrir o navegador.')
        try:
            web = BrowserV2(use_headless=False)
            web.navigate(url=url)
            log.info(f'Navegando na url: {url}')
            web.wait_element(xpath=self.input_cep)
            web.input(xpath=self.input_cep, send=self.cep)
            web.delay(start=2, end=4)
            web.click(xpath=self.btn_ok_cep)
            web.delay(start=10, end=15)

            if web.element_is_present(xpath=self.freight_error):
                err = web.get_text(xpath=self.freight_error)
                log.warning(f'Erro: {err}')
                web.close_driver()
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
            log.error(f'Ocorreu um erro ao tentar acessar o navegador.')
            web.close_driver()
