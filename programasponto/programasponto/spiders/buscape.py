from loguru import logger as log
from time import sleep
from http import HTTPStatus

import scrapy

from ..items import ProgramasPontoItem


class BuscapeSpider(scrapy.Spider):
    name = 'buscape'
    handle_httpstatus_list = [HTTPStatus.NOT_FOUND]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        log.info(f'Crawler iniciado: {self.name}')

        self.url = 'https://www.buscape.com.br/cupom-de-desconto/fast-shop-5'
        self.valor_bonus = '//div[@class="cashback-rate"]/text()'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        loja_nome = ''.join(response.url.split('/')[-1].split('-')[:-1])
        item = ProgramasPontoItem()
        item['loja_nome'] = loja_nome
        item['nome'] = self.name
        item['valor_bonus'] = response.xpath(self.valor_bonus).get().replace('%', '').strip()
        yield item
