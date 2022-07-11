import json
import os
from loguru import logger as log
from scrapy.exporters import JsonItemExporter
from itemadapter import ItemAdapter
import requests
import re

from .utils import clean_string_BRL, create_dirs, slug


class DefaultPipeline(object):
    def __init__(self):

        self.path_output = None
        self.path_base = None
        self.products = []
        self.fp = None
        self.exporter = None
        # self.exporter.start_exporting()

    def open_spider(self, spider):
        self.path_base = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', spider.name))
        self.path_output = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', spider.name, '{}'))

        create_dirs(self.path_base)
        self.fp = open(self.path_output.format(f'{slug(spider.keyword)}.json'), 'ab')  # Open the json file in wb mode
        self.exporter = JsonItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        self.exporter.start_exporting()

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

        #log.debug(f'{item["product_name"]}: preço: {item["product_price_sale"]}')
        if (item["product_price_sale"] > float(spider.price)) & (spider.freight != -1):
            self.products.append(item)

        return item

    def close_spider(self, spider):
        output = {
            'freight': spider.freight,
            'size': len(self.products),
            'products': self.products

        }

        self.to_db(items=output, spider=spider)
        self.exporter.export_item(output)
        self.exporter.finish_exporting()
        self.fp.close()
        log.info('Crawler finalizado.')

    def to_db(self, items, spider):
        log.info(f'Salvando os dados no banco de dados.')
        api_url = 'http://localhost:8000/api/v1/produtos/'
        headers = {'Content-Type': 'application/json'}
        for item in items['products']:
            item.pop('created_at', None)
            remove = 'Spider'
            name = re.sub(remove, '', spider.__class__.__name__)
            item.update({'id_loja': name})
            response = requests.post(api_url, data=json.dumps(ItemAdapter(item).asdict()), headers=headers)
            log.info(f'{response.status_code}: {response.text}')


class ShopsmilesPipeline(DefaultPipeline):
    pass


class ReedemPipeline(DefaultPipeline):

    def process_item(self, item, spider):
        log.info(f'Um novo item foi processado: {item["product_name"]}')
        self.products.append(item)
        return item

    def close_spider(self, spider):
        output = {
            'freight': spider.freight,
            'size': len(self.products),
            'products': self.products

        }
        self.to_db(items=output, spider=spider)
        self.exporter.export_item(output)
        self.exporter.finish_exporting()
        self.fp.close()
        log.info('Crawler finalizado.')
