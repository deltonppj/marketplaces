from loguru import logger as log
from programasponto.spiders.buscape import BuscapeSpider
from programasponto.spiders.latam import LatamSpider
from programasponto.spiders.esfera import EsferaSpider
from programasponto.spiders.dotz import DotzSpider
from programasponto.spiders.inter import InterSpider
from programasponto.spiders.livelo import LiveloSpider
from programasponto.spiders.meliuz import MeliuzSpider
from programasponto.spiders.tudoazul import TudoazulSpider

SPIDERS = [
    BuscapeSpider,
    LatamSpider,
    EsferaSpider,
    DotzSpider,
    InterSpider,
    LiveloSpider,
    MeliuzSpider,
    TudoazulSpider
]

URL_BASE_API = 'http://localhost:8000/api/v1/'
HEADERS = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjYwNDg3MDk3LCJpYXQiOjE2NTc4OTUwOTcsInN1YiI6IjEifQ.KfOdcM4tSvsJ8sAHHg12DufUygwxtGfF8NhGkNWc6Jc',
    'Content-Type': 'application/json'
}


def create_marketplaces_on_db():
    import re
    import requests
    from http import HTTPStatus

    for spider in SPIDERS:
        remove = 'Spider'
        name = re.sub(remove, '', spider.__name__)
        log.info(f'Criando {name} no banco de dados.')

        url = f'{URL_BASE_API}programaspontos'
        result = requests.post(url, json={'nome': name}, headers=HEADERS)

        if result.status_code == HTTPStatus.CREATED:
            log.info(f'{name} criado com sucesso!')
        else:
            log.error(f'{name} ocorreu um erro ao criar!')
            log.error(f'{result.text}')


if __name__ == '__main__':
    create_marketplaces_on_db()
