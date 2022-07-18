from loguru import logger as log
from time import sleep
from http import HTTPStatus
from urllib.parse import urlparse, unquote
import re

import scrapy

from ..items import ProgramasPontoItem


class TudoazulSpider(scrapy.Spider):
    name = 'tudoazul'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        log.info(f'Crawler iniciado: {self.name}')

        self.payload = {}
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',

        }

        self.urls = ['https://www.pontofrio.com.br/b2b/tudoazul.aspx',
                     'https://www.casasbahia.com.br/b2b/tudoazul.aspx',
                     'https://www.extra.com.br/b2b/tudoazul.aspx',
                     'https://m.clube.magazineluiza.com.br/selecao-produtos/clube-220419/se/?ordem=mais-vendidos&n=tudoazul&is_clube=1&menu=0&parceiro=tudoazul']

        self.img = '(//img[@data-u="image"])[1]/@src'
        self.img_magalu = '//div[@class="banner-hyper-top"]/img'

    def start_requests(self):
        for url in self.urls:
            log.info('Acessando: {}'.format(url))
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)
            sleep(1)

    def parse(self, response, **kwargs):
        item = ProgramasPontoItem()
        try:
            loja_nome = urlparse(response.url).netloc.split('.')[1]
            img_link = response.xpath(self.img).get()

            regex = r"-\d\w\d-"
            pts = re.findall(regex, img_link)[0].replace('-', '').split('x')

            item['loja_nome'] = loja_nome
            item['nome'] = self.name
            item['valor_bonus'] = pts[0]
            item['valor_real'] = pts[1]
        except:
            from uc_browser.browser_v2 import BrowserV2
            from selenium.webdriver.support.ui import WebDriverWait

            log.info('Abrindo navegador...')
            web = BrowserV2(use_headless=True)
            web.navigate(self.urls[3])
            WebDriverWait(web.driver, 15).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete")
            log.info('Pagina carregada com sucesso!')
            web.wait_to_click(xpath=self.img_magalu)
            loja_nome = urlparse(web.driver.current_url).netloc.split('.')[2]
            img_link = unquote(web.get_src(xpath=self.img_magalu))

            pts = img_link.split('TudoAzul_')[1].split(' ')[0]

            item['loja_nome'] = loja_nome
            item['nome'] = self.name
            item['valor_bonus'] = pts

        yield item
