from loguru import logger as log
import json
from time import sleep

import scrapy

from ..items import ProgramasPontoItem
from ..utils import clean_string_BRL


class DotzSpider(scrapy.Spider):
    name = 'dotz'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        log.info(f'Crawler iniciado: {self.name}')

        self.partners = {
            'americanas': 2,
            'submarino': 11,
            'shoptime': 53,
            'casasbahia': 77,
            'pontofrio': 76,
            'extra': 59,
            'maganizeluiza': 13,
        }

    def start_requests(self):
        for key, value in self.partners.items():
            url = 'https://api.dotz.com.br/capture/api/default/v2/partner/getbyid/{}'.format(str(value))
            log.info('Acessando: {}'.format(url))
            yield scrapy.Request(url=url, callback=self.parse)
            sleep(1)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)['data']

        loja_name = data['name']

        if data['name'] == 'Casas Bahia':
            loja_name = 'casasbahia'
        if data['name'] == 'Ponto':
            loja_name = 'pontofrio'
        if data['name'] == 'Magazine Luiza':
            loja_name = 'magazineluiza'

        item = ProgramasPontoItem()
        item['loja_nome'] = loja_name
        item['programa_pontos_nome'] = self.name
        item['valor_bonus'] = float(data['bonusNumberDotz'])
        item['valor_real'] = float(clean_string_BRL(data['bonusValueFor']).strip())

        yield item
