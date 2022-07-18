import argparse
import os, sys

from loguru import logger as log

from twisted.internet import reactor, defer

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from config import SPIDERS


@defer.inlineCallbacks
def crawl():
    settings = get_project_settings()
    # configure_logging()
    runner = CrawlerRunner(settings)

    if SPIDERS is None:
        log.error('No arquivo config.py é necessário informar uma lista de spiders.')
        sys.exit(os.EX_IOERR)

    for spider in SPIDERS:
        yield runner.crawl(spider)
    reactor.stop()


def main():
    crawl()
    reactor.run()


if __name__ == '__main__':
    log.info('Iniciando o sistema.')
    main()
