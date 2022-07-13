from loguru import logger as log
import json
import requests
import re

from itemadapter import ItemAdapter

_ENDPOINT = 'http://localhost:8000/api/v1/produtos/'
_HEADERS = {'Content-Type': 'application/json'}


class DefaultPipeline(object):

    def process_item(self, item, spider):
        log.info(f'Um novo item foi processado: {item["product_name"]}')
        try:
            if (spider.name != 'casasbahia') & (spider.name != 'extra') & \
                    (spider.name != 'pontofrio') & (spider.name != 'magazineluiza') & (spider.name != 'fastshop'):
                item["product_price_sale"] = float(clean_string_BRL(item["product_price_sale"]).strip())
                log.info(f'{item["product_name"]}: preço formatado.')
        except BaseException as err:
            log.error(f'Ocorreu um erro ao tentar converter o preço do produto: {item["product_price_sale"]}')
            log.error(err)

        # log.debug(f'{item["product_name"]}: preço: {item["product_price_sale"]}')
        if (item["product_price_sale"] > float(spider.price)) & (spider.freight != -1):
            log.info(f'Salvando os dados no banco de dados.')
            item.pop('created_at', None)
            remove = 'Spider'
            name = re.sub(remove, '', spider.__class__.__name__)
            item.update({'loja_nome': name})
            response = requests.post(_ENDPOINT, data=json.dumps(ItemAdapter(item).asdict()), headers=_HEADERS)
            log.info(f'{response.status_code}: {response.text}')

        return item
