import os
from loguru import logger as log
from scrapy.exporters import JsonItemExporter


class AmericanasPipeline(object):
    def __init__(self):
        self.path_output = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output', '{}'))
        self.fp = open(self.path_output.format('americanas.json'), 'wb')  # Open the json file in wb mode
        self.exporter = JsonItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')
        self.exporter.start_exporting()

    def open_spider(self, spider):
        log.info('Crawler iniciado.')

    def process_item(self, item, spider):
        log.info('Um novo item foi processado.')
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()
        log.info('Crawler finalizado.')
