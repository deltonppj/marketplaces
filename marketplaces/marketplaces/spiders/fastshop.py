import time
import os
import json
import requests
from loguru import logger as log
from datetime import datetime
from http import HTTPStatus


import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse

from urllib.parse import urlparse
from uc_browser.browser_v2 import BrowserV2

from ..items import DefaultItem
from ..utils import slug

'''
Os produtos do Fastshop são carregados em páginas separadas.
Para isso, é necessário em primeiro lugar verificar se o retorno do termo pesquisado faz parte ou não de um catalago 
de produtos regionalizado (regionalizedResult)

Quando o produto faz parte o servidor retorna uma url que sera apresentada no front mas dessa url so vamos pegar o id
do catalago regionalizado e passa-lo como argumento para o web service.

Além os preços também são processados em endpoints separados, sendo necessário passar o sku para obter os preços.
Os preços dependendo do produto estão armazenados em chave/valor diferentes.

Para acessar a pagina de detalhes esse é o padrão:
https://www.fastshop.com.br/web/p/d/sku/slug(product_name)

Paginação tambem é diferente para as duas situações comentadas acima.

'''

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', '{}', '{}'))


class FastshopSpider(scrapy.Spider):
    name = 'fastshop'

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

        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'referer': 'https://www.fastshop.com.br/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'

        }

        self.meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}
        self.page = 1
        self.url = f'https://apigw.fastshop.com.br/product/v0/regionalized/v1/catalog/by-search?terms={self.keyword}&page={self.page}'
        self.Key = None

    def start_requests(self):
        '''
        Neste primeiro request é que vamos ver se o termo pesquisado faz parte de um catalago regionalizado.
        '''
        log.info('Buscando chave de acesso ao catálogo...')
        log.info(f'Pagina: {self.url}')
        yield scrapy.Request(
            url=self.url,
            callback=self.parse,
            meta=self.meta,
            headers=self.headers)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        try:
            next_pagination = data.get('pagination')['next']
        except:
            CloseSpider('Pagina não encontrada.')

        try:
            if data['regionalizedResult'] is False:
                products = data.get('products')
                log.debug(f'Produtos encontrados: {len(products)}')

                for product in products:
                    is_available = product['status']

                    if is_available == 'AVAILABLE':
                        product_sku = product['id']
                        product_name = product['name']
                        product_url = product['url']

                        product_item = {
                            'name': product_name,
                            'url': product_url,
                            'sku': product_sku
                        }
                        # Pegando preco do produto
                        url = f'https://apigw.fastshop.com.br/price/v0/management/price-promotion/price?store=fastshop&channel=webapp&skus={product_sku}'
                        yield scrapy.Request(
                            url=url,
                            method='GET',
                            headers=self.headers,
                            callback=self.parse_price,
                            cb_kwargs={'product_item': product_item})

                self.page += 1
                self.url = f'https://apigw.fastshop.com.br/product/v0/regionalized/v1/catalog/by-search?terms={self.keyword}&page={self.page}'
                log.info(f'Pagina: {self.page} - {self.url}')
                yield scrapy.Request(url=self.url, callback=self.parse, meta=self.meta, headers=self.headers)
        except:
            # Regionalizado
            self.Key = data['link'].split('/')[-2]
            url = f'https://apigw.fastshop.com.br/product/v0/regionalized/v1/catalog/by-category?category={self.Key}&pageNumber={self.page}'
            log.info('Chave de acesso encontrada...')
            log.info(f'Pagina: {url}')

            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse_regionalized_products,
            )

    def parse_regionalized_products(self, response):
        if response.status == HTTPStatus.NOT_FOUND:
            log.warning(f'Não existem produtos nesta página.')
            raise CloseSpider('Pagina não encontrada.')

        data = json.loads(response.text)
        products = data.get('products')
        log.debug(f'Produtos encontrados: {len(products)}')

        for product in products:
            is_available = product['buyable']

            if is_available:
                product_partNumber = product['partNumber']
                product_name = product['shortDescription']
                product_url = f'https://www.fastshop.com.br/web/p/d/{product_partNumber}/{slug(product_name)}'

                product_item = {
                    'name': product_name,
                    'url': product_url,
                    'sku': product_partNumber
                }
                # Pegando preco do produto
                url = f'https://apigw.fastshop.com.br/price/v0/management/price-promotion/price?store=fastshop&channel=webapp&skus={product_partNumber}'
                yield scrapy.Request(
                    url=url,
                    method='GET',
                    headers=self.headers,
                    callback=self.parse_price,
                    cb_kwargs={'product_item': product_item})

        self.page += 1
        url = f'https://apigw.fastshop.com.br/product/v0/regionalized/v1/catalog/by-category?category={self.Key}&pageNumber={self.page}'
        log.info(f'Pagina: {self.page} - {url}')
        yield scrapy.Request(
            url=url,
            method='GET',
            headers=self.headers,
            callback=self.parse_regionalized_products)

    def parse_price(self, response, product_item):
        data = json.loads(response.text)

        try:
            price = data['result'][0]['products'][0]['skus'][0]['promotions'][0]['value']
        except:
            try:
                price = data['result'][0]['products'][0]['skus'][0]['price']['offerPrice']
            except:
                log.debug(product_item['url'])
                log.error(f'Erro ao acessar preço do produto: {product_item["sku"]}')

        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        item = DefaultItem()
        item['created_at'] = str(today)
        item['product_sku'] = product_item['sku'].split('_')[0]
        item['product_name'] = product_item['name']
        item['product_price_sale'] = price
        item['product_url'] = product_item['url']

        yield item

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
