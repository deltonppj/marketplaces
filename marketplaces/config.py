from marketplaces.spiders.americanas import AmericanasSpider
from marketplaces.spiders.casasbahia import CasasbahiaSpider
from marketplaces.spiders.extra import ExtraSpider
from marketplaces.spiders.pontofrio import PontofrioSpider
from marketplaces.spiders.submarino import SubmarinoSpider
from marketplaces.spiders.shoptime import ShoptimeSpider

SPIDERS = [
    AmericanasSpider,
    CasasbahiaSpider,
    ExtraSpider,
    PontofrioSpider,
    SubmarinoSpider,
    ShoptimeSpider
    ]

KEYWORDS = [
    'iphone -p 5000',
    'iphone 11 -p 3000',
    'luva de box -p 50',
    'bicicleta infantil aro 16 -p 300'
]

VALIDATE_FREIGHT = False