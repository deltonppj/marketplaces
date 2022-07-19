from loguru import logger as log
import json
import requests
import re
from itemadapter import ItemAdapter


_ENDPOINT_PP = 'http://localhost:8000/api/v1/pp/'
_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjg5NDYwMjQ5LCJpYXQiOjE2NTc5MjQyNDksInN1YiI6IjEifQ.5jrfdm7N5Kt9G4IdNpCLBOpDauwPRmfNuEac5dcjgQc'
}


class ProgramasPontoPipeline(object):
    def process_item(self, item, spider):
        log.info('Processando item: {}'.format(item['nome']))
        log.debug(item)
        return item
