import scrapy
from scrapy.exceptions import CloseSpider

from urllib.parse import urlparse

from ..items import AmericanasItem


class AmericanasSpider(scrapy.Spider):
    name = 'americanas'
    allowed_domains = ['americanas.com.br']

    query_filter = '?filter=%7B"id"%3A"loja"%2C"value"%3A"1p%7CAmericanas%7Cb2w.loja"%2C"fixed"%3Afalse%7D&sortBy=relevance'
    query_offset = '&limit=24&offset={}'
    offset = 0
    keyword = 'iphone'
    urls = [f'https://americanas.com.br/busca/{keyword}{query_filter}{query_offset.format(offset)}']

    cards = '//*[contains(@class, "ColGridItem")]'
    product_url = '//*[contains(@class, "ColGridItem")]//a/@href'
    product_name = './/*[contains(@class, "product-name")]/text()'
    product_price_sale = './/*[contains(@class, "PromotionalPrice")]/text()'
    limit_page = '//*[contains(text(), "poxa, nenhum resultado encontrado para ")]'

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        print(f'Offset: {self.offset}')
        has_page = response.xpath(self.limit_page).get()
        if has_page:
            raise CloseSpider('All page was scraped.')

        parsed_uri = urlparse(response.url)
        url_base = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

        cards = response.xpath(self.cards)
        for card in cards:
            item = AmericanasItem()
            item['product_name'] = card.xpath(self.product_name).get()
            item['product_price_sale'] = card.xpath(self.product_price_sale).get()
            item['product_url'] = url_base + card.xpath(self.product_url).get()

            yield item

        self.offset += 24
        yield scrapy.Request(
            url=f'https://americanas.com.br/busca/{self.keyword}{self.query_filter}{self.query_offset.format(self.offset)}',
            callback=self.parse
        )



