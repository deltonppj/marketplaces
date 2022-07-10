from loguru import logger as log

SPIDERS = [
    'tudoazul',
    'esfera',
    'livelo',
    'dotz',
    'latam',
    'inter',
    'meliuz',
    'buscape'
]

KEYWORDS = [

]

URL_BASE_API = 'http://localhost:8000/api/v1/'


def create_programas_on_db():
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