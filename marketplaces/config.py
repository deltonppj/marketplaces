from marketplaces.spiders.americanas import AmericanasSpider
from marketplaces.spiders.casasbahia import CasasbahiaSpider
from marketplaces.spiders.extra import ExtraSpider
from marketplaces.spiders.pontofrio import PontofrioSpider
from marketplaces.spiders.submarino import SubmarinoSpider
from marketplaces.spiders.shoptime import ShoptimeSpider
from marketplaces.spiders.magazineluiza import MagazineluizaSpider
from marketplaces.spiders.fastshop import FastshopSpider
from marketplaces.spiders.shopsmiles import ShopsmilesSpider
from marketplaces.spiders.redeem import ReedemSpider
from marketplaces.spiders.shoptudoazul import ShoptudoazulSpider

SPIDERS = [
    AmericanasSpider,
    CasasbahiaSpider,
    ExtraSpider,
    PontofrioSpider,
    SubmarinoSpider,
    ShoptimeSpider,
    MagazineluizaSpider,
    FastshopSpider,
    ShopsmilesSpider,
    ReedemSpider,
    ShoptudoazulSpider
    ]

KEYWORDS = [
    # 'dell g15 -p 4000',
    # 'iphone -p 5000',
    'iphone 11 -p 3000',
    # 'luva de box -p 50',
    # 'bicicleta -p 300'
]

VALIDATE_FREIGHT = False