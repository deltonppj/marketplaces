import time

from loguru import logger as log
from datetime import datetime
import json

import scrapy
import os

from scrapy.exceptions import CloseSpider

from urllib.parse import urlparse
from uc_browser.browser_v2 import BrowserV2

from ..items import DefaultItem

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', '{}', '{}'))


class MagazineluizaSpider(scrapy.Spider):
    name = 'magazineluiza'
    custom_settings = {'ITEM_PIPELINES': {'marketplaces.pipelines.DefaultPipeline': 300}}

    log.add(PATH.format(name, f'{name}.log'))

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

        self.filter = 'filters=seller---magazineluiza'

        self.keyword = search
        log.info(f'Palavra chave informada: {self.keyword}')

        self.url = 'https://www.magazineluiza.com.br/'
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }
        self.key = None

    def start_requests(self):
        log.info('Buscando chave de acesso ao catálogo...')
        log.info(f'Pagina: {self.url}')
        yield scrapy.Request(url=self.url, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):
        self.key = response.xpath('//script[contains(@src, "_ssg")]/@src').get().split('/')[4]

        if self.key is None:
            raise CloseSpider('Não foi possível obter a chave de acesso.')

        url = f'https://www.magazineluiza.com.br/_next/data/{self.key}/busca/{self.keyword}.json?page=1&{self.filter}&slug=busca&slug={self.keyword}'
        log.info('Acessando...')
        log.info(f'Pagina: {url}')
        yield scrapy.Request(
            url=url,
            headers=self.headers,
            callback=self.parse_products)

    def parse_products(self, response):
        data = json.loads(response.text)
        products = data['pageProps']['data']['search']['products']

        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        parsed_uri = urlparse(response.url)
        url_base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        for product in products:
            item = DefaultItem()
            item['created_at'] = str(today)
            item['product_sku'] = product['seller']['sku']
            item['product_name'] = product['title']
            item['product_price_sale'] = float(product['price']['bestPrice'])
            item['product_url'] = url_base + '/' + product['url']

            if self.validate_freight:
                if (self.freight is None) | (self.freight == -1):
                    self.set_freight(url=url_base + '/' + product['url'])

            yield item

        next_page = (data['pageProps']['data']['search']['pagination']['page'] + 1)
        total_page = data['pageProps']['data']['search']['pagination']['pages']

        if next_page <= total_page:
            url = f'https://www.magazineluiza.com.br/_next/data/{self.key}/busca/{self.keyword}.json?page={next_page}&{self.filter}&slug=busca&slug={self.keyword}'
            log.info(f'Pagina: {url}')
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse_products)

    def set_freight(self, url):
        log.info('Preparando para abrir o navegador.')
        try:
            web = BrowserV2(use_headless=False)
            web.navigate(url=url)
            log.info(f'Navegando na url: {url}')
            web.wait_to_click(xpath=self.cookie_accept, time=15)
            web.input_like_a_human(xpath=self.input_cep, send=self.cep)
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
            log.error(f'Ocorreu um erro ao tentar acessar o navegador. {err}')
