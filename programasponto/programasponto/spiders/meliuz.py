from loguru import logger as log
from time import sleep
from http import HTTPStatus
from uc_browser.browser_v2 import BrowserV2

import scrapy
from selenium.webdriver.support.ui import WebDriverWait

from ..items import ProgramasPontoItem
from ..utils import extract_numbers


class MeliuzSpider(scrapy.Spider):
    name = 'meliuz'
    handle_httpstatus_list = [HTTPStatus.NOT_FOUND]
    custom_settings = {
        'COOKIES_ENABLED': True,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        log.info(f'Crawler iniciado: {self.name}')

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'content-encoded': 'gzip',
        }

        self.partners = {
            'AMC': 'americanas',
            'SBC': 'submarino',
            'STC': 'shoptime',
            'CSB': 'casas-bahia',
            'PTF': 'ponto',
            'EXT': 'extra',
            'MZL': 'magazine-luiza',
        }
        self.valor_bonus = '//button[@id="button-active-cashback" and @class="button partner-pg__header-section-active-btn-desktop"]/text()'
        self.url = 'https://www.meliuz.com.br/'

        log.info('Abrindo navegador...')
        self.web = BrowserV2(use_headless=True)
        self.web.navigate(self.url)
        WebDriverWait(self.web.driver, 15).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete")
        log.info('Pagina carregada com sucesso!')

    def start_requests(self):
        for key, value in self.partners.items():
            url = 'https://www.meliuz.com.br/desconto/cupom-{}'.format(str(value))
            log.info('Acessando: {}'.format(url))
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.web.get_cookies())
            sleep(1)

    def parse(self, response, **kwargs):
        loja_nome = response.url.split('cupom-')[-1]
        if int(response.status) == HTTPStatus.NOT_FOUND:
            log.info(f'{loja_nome}: Programa de pontos não encontrado')
        else:
            item = ProgramasPontoItem()
            if response.url.split('cupom-')[-1] == 'ponto':
                loja_nome = 'pontofrio'
            if response.url.split('cupom-')[-1] == 'magazine-luiza':
                loja_nome = 'maganizeluiza'
            if response.url.split('cupom-')[-1] == 'casas-bahia':
                loja_nome = 'casasbahia'

            item['loja_nome'] = loja_nome
            item['nome'] = self.name
            item['valor_bonus'] =  extract_numbers(response.xpath(self.valor_bonus).get())

            yield item
