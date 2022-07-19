from loguru import logger as log
import json
from time import sleep

import scrapy

from ..items import ProgramasPontoItem


class LiveloSpider(scrapy.Spider):
    name = 'livelo'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        log.info(f'Crawler iniciado: {self.name}')

        self.partners = {
            'AMC': 'americanas',
            'SBC': 'submarino',
            'STC': 'shoptime',
            'CSB': 'casasbahia',
            'PTF': 'pontofrio',
            'EXT': 'extra',
            'MZL': 'magazineluiza',
        }

    def start_requests(self):
        for key, value in self.partners.items():
            url = 'https://apis.pontoslivelo.com.br/partners-campaign/v1/campaigns/active?partnersCodes={}'.format(str(key))
            log.info('Acessando: {}'.format(url))
            yield scrapy.Request(url=url, callback=self.parse)
            sleep(1)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)[0]
        item = ProgramasPontoItem()
        item['loja_nome'] = self.partners.get(response.url.split('=')[1])
        item['programa_pontos_nome'] = self.name
        item['valor_bonus'] = float(data['parity'])
        item['valor_real'] = float(data['value'])

        yield item
