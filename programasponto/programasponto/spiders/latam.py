from loguru import logger as log
from time import sleep
from http import HTTPStatus

import scrapy

from ..items import ProgramasPontoItem


class LatamSpider(scrapy.Spider):
    name = 'latam'
    handle_httpstatus_list = [HTTPStatus.NOT_FOUND]

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
            'MZL': 'magalu',
        }
        self.valor_bonus = '(//div[@class="info-junte-topo"]/h2/text())[1]'
        self.valor_real = '(//div[@class="info-junte-topo"]/h2/text())[2]'

    def start_requests(self):
        for key, value in self.partners.items():
            url = 'https://latampass.latam.com/pt_br/junte-pontos/{}'.format(str(value))
            log.info('Acessando: {}'.format(url))
            yield scrapy.Request(url=url, callback=self.parse)
            sleep(1)

    def parse(self, response, **kwargs):
        loja_nome = response.url.split('/')[-1]
        if int(response.status) == HTTPStatus.NOT_FOUND:
            log.info(f'{loja_nome}: Programa de pontos não encontrado')
        else:
            item = ProgramasPontoItem()
            if response.url.split('/')[-1] == 'ponto':
                loja_nome = 'pontofrio'
            if response.url.split('/')[-1] == 'magalu':
                loja_nome = 'magazineluiza'
            if response.url.split('/')[-1] == 'casas-bahia':
                loja_nome = 'casasbahia'

            item['loja_nome'] = loja_nome
            item['programa_pontos_nome'] = self.name
            item['valor_bonus'] = float(response.xpath(self.valor_bonus).get())
            item['valor_real'] = float(response.xpath(self.valor_real).get())

            yield item
