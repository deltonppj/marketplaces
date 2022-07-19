from loguru import logger as log
import json
from time import sleep

import scrapy

from ..items import ProgramasPontoItem


class InterSpider(scrapy.Spider):
    name = 'inter'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        log.info(f'Crawler iniciado: {self.name}')

        self.partners = {
            'AMC': 'americanas',
            'SBC': 'submarino',
            'STC': 'shoptime',
            'CSB': 'casas-bahia',
            'PTF': 'ponto',
            'EXT': 'extra',
            'MZL': 'magazine-luiza',
        }

    def start_requests(self):
        for key, value in self.partners.items():
            url = 'https://marketplace-api.web.bancointer.com.br/site/affiliate/inter/v1/stores/slug/{}?lang=pt-BR'.format(
                str(value))
            log.info('Acessando: {}'.format(url))
            yield scrapy.Request(url=url, callback=self.parse)
            sleep(1)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        loja_nome = data['slug']
        if data['slug'] == 'ponto':
            loja_nome = 'pontofrio'
        if data['slug'] == 'magazine-luiza':
            loja_nome = 'magazineluiza'
        if data['slug'] == 'casas-bahia':
            loja_nome = 'casasbahia'

        item = ProgramasPontoItem()
        item['loja_nome'] = loja_nome
        item['programa_pontos_nome'] = self.name
        item['valor_bonus'] = float(data['storeCashbacks']['fullCashbackValue'])
        item['valor_real'] = float(0)  # data['storeCashbacks']['partialCashbackValue']
        yield item
