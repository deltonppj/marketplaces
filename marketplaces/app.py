import argparse
import os, sys

from loguru import logger as log

from twisted.internet import reactor, defer

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from marketplaces.spiders.americanas import AmericanasSpider
from marketplaces.spiders.casasbahia import CasasbahiaSpider


def get_argument():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-s', '--search', help='Palavra chave a ser pesquisada.')
    arg_parser.add_argument('-f', '--filter', help='Filtro para pesquisa.')
    arg_parser.add_argument('-F', '--file', help='Arquivo contendo uma lista de palavras chave.')
    arg_parser.add_argument('-p', '--price', help='Filtro para o preco.')
    arg_parser.add_argument('-v',
                            '--validar-frete',
                            nargs='?',
                            const=True,
                            help='Buscar preço do frete.')

    args = arg_parser.parse_args()
    return args


@defer.inlineCallbacks
def crawl(search=None, filter=None, price=None, validate_freight=None):
    settings = get_project_settings()
    #configure_logging()
    runner = CrawlerRunner(settings)

    if type(search) is list:
        for s in search:
            splited = s.split('-p')
            search = splited[0].strip() # keyword
            price = splited[1].strip() # price

            yield runner.crawl(AmericanasSpider, search=search, filter=filter, price=price, validate_freight=validate_freight)
            yield runner.crawl(CasasbahiaSpider, search=search, filter=filter, price=price, validate_freight=validate_freight)
        reactor.stop()

    else:
        yield runner.crawl(AmericanasSpider, search=search, filter=filter, price=price, validate_freight=validate_freight)
        yield runner.crawl(CasasbahiaSpider, search=search, filter=filter, price=price, validate_freight=validate_freight)
        reactor.stop()


def read_file(file):
    try:
        return list(map(str.strip, open(file).readlines()))
    except BaseException as err:
        log.error(err)


def main():
    search = get_argument().search
    filter = get_argument().filter
    price = get_argument().price
    validate_freight = get_argument().validar_frete
    file = get_argument().file

    try:
        if (file is None) & (search is None):
            raise TypeError('É necessário informar uma palavra chave(-s) ou um arquivo txt(-F).')
        if (file is not None) & (search is not None):
            raise TypeError('É necessário informar ou uma palavra chave(-s) ou um arquivo txt(-F).')
        if (search is not None) & (price is None):
            raise TypeError('Para pesquisa manual é necessário informar um preço.(-p)')
    except TypeError as err:
        log.error(err)
        sys.exit(os.EX_IOERR)

    if file:
        search = read_file(file)

    crawl(search, filter, price, validate_freight)
    reactor.run()


if __name__ == '__main__':
    log.info('Iniciando o sistema.')
    main()
