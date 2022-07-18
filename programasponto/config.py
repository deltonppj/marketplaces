from loguru import logger as log
from programasponto.spiders.buscape import BuscapeSpider
from programasponto.spiders.latam import LatamSpider
from programasponto.spiders.esfera import EsferaSpider
from programasponto.spiders.dotz import DotzSpider
from programasponto.spiders.inter import InterSpider
from programasponto.spiders.livelo import LiveloSpider
from programasponto.spiders.meliuz import MeliuzSpider


SPIDERS = [
    BuscapeSpider,
    LatamSpider,
    EsferaSpider,
    DotzSpider,
    InterSpider,
    LiveloSpider,
    MeliuzSpider
]
