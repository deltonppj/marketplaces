from marketplaces.spiders.americanas import AmericanasSpider
from marketplaces.spiders.casasbahia import CasasbahiaSpider
from marketplaces.spiders.extra import ExtraSpider
from marketplaces.spiders.pontofrio import PontofrioSpider
from marketplaces.spiders.submarino import SubmarinoSpider
from marketplaces.spiders.shoptime import ShoptimeSpider
from marketplaces.spiders.magazineluiza import MagazineluizaSpider
from marketplaces.spiders.fastshop import FastshopSpider
from marketplaces.spiders.shopsmiles import ShopsmilesSpider
from marketplaces.spiders.redeem import ReedemSpider
from marketplaces.spiders.shoptudoazul import ShoptudoazulSpider

from loguru import logger as log

SPIDERS = [
    AmericanasSpider,
    # CasasbahiaSpider,
    # ExtraSpider,
    # PontofrioSpider,
    # SubmarinoSpider,
    # ShoptimeSpider,
    # MagazineluizaSpider,
    # FastshopSpider,
    # ShopsmilesSpider,
    # ReedemSpider,
    # ShoptudoazulSpider
]

KEYWORDS = [
    # 'dell g15 -p 4000',
    # 'iphone -p 5000',
    'iphone 11 -p 3000',
    # 'luva de box -p 50',
    # 'bicicleta -p 300'
]

VALIDATE_FREIGHT = False
URL_BASE_API = 'http://localhost:8000/api/v1/'


def create_marketplaces_on_db():
    import re
    import requests
    from http import HTTPStatus

    for spider in SPIDERS:
        remove = 'Spider'
        name = re.sub(remove, '', spider.__name__)
        log.info(f'Criando {name} no banco de dados.')

        url = f'{URL_BASE_API}lojas'
        result = requests.post(url, json={'nome': name})

        if result.status_code == HTTPStatus.CREATED:
            log.info(f'{name} criado com sucesso!')
        else:
            log.error(f'{name} ocorreu um erro ao criar!')
            lof.error(f'{result.text}')


if __name__ == '__main__':
    create_marketplaces_on_db()