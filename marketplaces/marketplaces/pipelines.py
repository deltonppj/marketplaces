import os
from loguru import logger as log
from scrapy.exporters import JsonItemExporter

from .utils import clean_string_BRL


class AmericanasPipeline(object):
    def __init__(self):
        self.path_output = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', '{}'))
        self.fp = open(self.path_output.format('americanas.json'), 'wb')  # Open the json file in wb mode
        self.exporter = JsonItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        self.exporter.start_exporting()

    def open_spider(self, spider):
        log.info('Crawler iniciado.')

    def process_item(self, item, spider):
        log.info(f'Um novo item foi processado: {item["product_name"]}')
        try:
            item["product_price_sale"] = clean_string_BRL(item["product_price_sale"]).strip()
            log.info(f'{item["product_name"]}: preço formatado.')
        except BaseException as err:
            log.error(f'Ocorreu um erro ao tentar converter o preço do produto: {item["product_price_sale"]}')
            log.error(err)

        price = '1000'
        if item["product_price_sale"] > price:
            self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()
        log.info('Crawler finalizado.')


