import os
from loguru import logger as log
from scrapy.exporters import JsonItemExporter

from .utils import clean_string_BRL, create_dirs, slug


class AmericanasPipeline(object):
    def __init__(self):
        self.path_base = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'americanas'))
        self.path_output = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', 'americanas', '{}'))
        self.fp = None
        self.exporter = None
        # self.exporter.start_exporting()

    def open_spider(self, spider):
        log.info('Crawler iniciado.')
        create_dirs(self.path_base)

        self.fp = open(self.path_output.format(f'{slug(spider.keyword)}.json'), 'ab')  # Open the json file in wb mode
        self.exporter = JsonItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        log.info(f'Um novo item foi processado: {item["product_name"]}')
        try:
            item["product_price_sale"] = float(clean_string_BRL(item["product_price_sale"]).strip())
            log.info(f'{item["product_name"]}: preço formatado.')
        except BaseException as err:
            log.error(f'Ocorreu um erro ao tentar converter o preço do produto: {item["product_price_sale"]}')
            log.error(err)

        if item["product_price_sale"] > float(spider.price):
            self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()
        log.info('Crawler finalizado.')


