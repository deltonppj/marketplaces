from loguru import logger as log
import json

import scrapy

from ..items import ProgramasPontoItem


class EsferaSpider(scrapy.Spider):
    name = 'esfera'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        log.info(f'Crawler iniciado: {self.name}')

        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'content-type': 'application/json',
            'accept-encoding': 'gzip, deflate, br',
        }
        self.query = '?dataOnly=true&cacheableDataOnly=false&productTypesRequired=false'
        self.urls = [f'https://www.esfera.com.vc/ccstoreui/v1/pages/p/casasbahia/e000100177{self.query}',
                     f'https://www.esfera.com.vc/ccstoreui/v1/pages/p/extracom/e000100178{self.query}',
                     f'https://www.esfera.com.vc/ccstoreui/v1/pages/p/ponto/e000100179{self.query}',
                     f'https://www.esfera.com.vc/ccstoreui/v1/pages/p/magalu/e000100100{self.query}']

    def start_requests(self):
        for url in self.urls:
            log.info('Acessando: {}'.format(url))
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        pts = data['data']['page']['product']['esf_accumulationFactor'].split(' ')[0].split('x')
        loja_nome = response.url.split('/')[7]

        if response.url.split('/')[7] == 'magalu':
            loja_nome = 'magazineluiza'
        if response.url.split('/')[7] == 'ponto':
            loja_nome = 'pontofrio'

        item = ProgramasPontoItem()
        item['loja_nome'] = loja_nome
        item['nome'] = self.name
        item['valor_bonus'] = pts[0]
        item['valor_real'] = pts[1]
        yield item
