from loguru import logger as log
import json
import requests
import re

from itemadapter import ItemAdapter

_ENDPOINT_PP = 'http://localhost:8000/api/v1/programaspontos/loja'
_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjg5ODI5NTUwLCJpYXQiOjE2NTgyOTM1NTAsInN1YiI6IjEifQ.sDTE5G0TMB4IK5VniynYCIGAd6NZ-97dKc3pa6vT80g'
}


class ProgramasPontoPipeline(object):
    def process_item(self, item, spider):
        log.info('Processando item: {}'.format(item['loja_nome']))

        log.info(f'Salvando os dados no banco de dados.')
        remove = 'Spider'
        name = re.sub(remove, '', spider.__class__.__name__)
        item.update({'programa_pontos_nome': name})
        response = requests.post(_ENDPOINT_PP, data=json.dumps(ItemAdapter(item).asdict()), headers=_HEADERS)
        log.info(f'{response.status_code}: {response.text}')

        return item

