import argparse
import os.path
from loguru import logger as log

from twisted.internet import reactor, defer

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from marketplaces.spiders.americanas import AmericanasSpider


def get_argument():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-s', '--search', help='Palavra chave a ser pesquisada.', required=True)
    arg_parser.add_argument('-f', '--filter', help='Filtro para pesquisa.')
    arg_parser.add_argument('-p', '--price', help='Filtro para o preco.', required=True)

    args = arg_parser.parse_args()
    return args


@defer.inlineCallbacks
def crawl(search=None, filter=None, price=None):
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    yield runner.crawl(AmericanasSpider, search=search, filter=filter, price=price)
    reactor.stop()


def main():
    search = get_argument().search
    filter = get_argument().filter
    price = get_argument().price

    crawl(search, filter, price)
    reactor.run()


if __name__ == '__main__':
    log.info('Iniciando o sistema.')
    main()
