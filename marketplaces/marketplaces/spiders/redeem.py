import time
from time import sleep
import os
import json
import requests
from loguru import logger as log
from datetime import datetime
from http import HTTPStatus

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse
from scrapy.selector import Selector

from urllib.parse import urlparse
from uc_browser.browser_v2 import BrowserV2
from selenium.webdriver.common.by import By

from ..items import RedeemItem
from ..utils import slug

'''
    Raspagem de dado atraves de webdriver.
    Em uma possivel futura versao, sera utilizado o scrapy.

    Paginação inviabilizou o processo de raspagem via scrapy.
'''


class ReedemSpider(scrapy.Spider):
    name = 'reedem'
    custom_settings = {'ITEM_PIPELINES': {'marketplaces.pipelines.ReedemPipeline': 300}}
    start_urls = [
        'https://www.shoppingsmiles.com.br/smiles/super_busca.jsf?b=iphone&a=false']  # Fakely wait to load the page

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

        self.page = 1
        self.url = f'https://www.shoppingsmiles.com.br/smiles/super_busca.jsf?b={self.keyword}&a=false'
        log.info(f'Preparando para carregar todo conteúdo do site: {self.url}')

        self.web = BrowserV2(use_headless=False)
        self.control_visible_btn = '//span[@class="btn-carregar-mais"]'
        self.btn_load_more = '//button[contains(@onclick, "content_mais_footer")]'
        self.hide_loding_modal = '//div[contains(@class, "ui-hidden-container modal-loading")]'
        self.card_products = '//span[@class="box-produto"]'
        self.product_url = './div/a/@href'
        self.product_name = './/span[contains(@class, "product-name-busca")]/span/text()'
        self.product_price_miles = './/span[contains(@id, "precoProduto")]/span/following-sibling::span/text()'
        self.product_discount = './/span[contains(@class, "com-clube-smiles")]/span/span[3]/text()'

        log.info('Abrindo navegador...')
        self.web.navigate(url=self.url)

        try:
            self.is_btn = self.web.driver.find_element(By.XPATH, value=self.control_visible_btn).get_attribute('style')
            while self.is_btn != 'display: none;':
                log.info(f'Carregando pagina: {self.page}')
                self.web.wait_element(xpath=self.btn_load_more)
                if self.web.element_is_present(xpath=self.btn_load_more):
                    self.web.click(xpath=self.btn_load_more)
                    sleep(3)
                    self.screen_loding = self.web.driver.find_element(By.XPATH,
                                                                      value=self.hide_loding_modal).get_attribute(
                        'aria-live')
                    if self.screen_loding == 'polite':
                        # caso ainda esteja carregando, espera 6 segundos
                        sleep(6)
                    self.is_btn = self.web.driver.find_element(By.XPATH, value=self.control_visible_btn).get_attribute(
                        'style')  # noqa
                else:
                    log.info('Não existe mais páginas para carregar.')
                self.page += 1
        except Exception as err:
            log.error(f'Erro ao carregar página: {self.page}')

        self.html = self.web.driver.page_source

        try:
            self.web.close_driver()
            log.info('Navegador fechado.')
        except Exception as err:
            log.error(f'Erro ao fechar navegador: {err}')

    def parse(self, response, **kwargs):
        response = Selector(text=self.html)
        parsed_uri = urlparse(self.url)
        url_base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        cards = response.xpath(self.card_products)
        for card in cards:
            product_price_miles = card.xpath(self.product_price_miles).get()
            product_discount = card.xpath(self.product_discount).get()
            product_reedem = float(product_price_miles) - float(product_discount)

            item = RedeemItem()
            item['created_at'] = str(today)
            item['product_sku'] = card.xpath(self.product_url).get().split('&p=')[1].split('&n=')[0].split('_')[
                0]  # Split para pegar o sku do produto # noqa
            item['product_name'] = card.xpath(self.product_name).get()
            item['product_reedem'] = round(product_reedem, 3)
            item['product_url'] = url_base + card.xpath(self.product_url).get()

            yield item
