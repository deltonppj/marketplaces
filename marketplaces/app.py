import argparse
import os, sys

from loguru import logger as log

from twisted.internet import reactor, defer

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from marketplaces.spiders.redeem import ReedemSpider
from config import KEYWORDS, SPIDERS, VALIDATE_FREIGHT


@defer.inlineCallbacks
def crawl():
    settings = get_project_settings()
    #configure_logging()
    runner = CrawlerRunner(settings)

    if SPIDERS is None:
        log.error('No arquivo config.py é necessário informar uma lista de spiders.')
        sys.exit(os.EX_IOERR)
    elif KEYWORDS is None:
        log.error('No arquivo config.py é necessário passar uma lista de keywords.')
        sys.exit(os.EX_IOERR)
    elif VALIDATE_FREIGHT:
        log.error('No arquivo config.py é necessário informar a opção de frete. (Eg. VALIDATE_FREIGHT = True)')
        sys.exit(os.EX_IOERR)

    if type(KEYWORDS) is list:
        for s in KEYWORDS:
            splited = s.split('-p')
            search = splited[0].strip()  # keyword
            #price = splited[1].strip()  # price

            for spider in SPIDERS:
                price = splited[1].strip()
                if spider.__name__ == ReedemSpider.__name__:
                    price = 0
                yield runner.crawl(spider, search=search, filter=None, price=price, validate_freight=VALIDATE_FREIGHT)
        reactor.stop()


def main():
    crawl()
    reactor.run()


if __name__ == '__main__':
    log.info('Iniciando o sistema.')
    main()
