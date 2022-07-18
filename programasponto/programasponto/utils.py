from loguru import logger as log

from scrapy.exceptions import CloseSpider

import re
import os
import unicodedata


def extract_numbers(text):
    return re.findall(r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', text) # commas, dots, and integers


def clean_string_BRL(data):
    '''Convert from this format R$0.00 to 0.00'''
    string = re.sub('R\$|\.', '', data)
    string = re.sub(',', '.', string)
    return string


def create_dirs(dirs):
    try:
        if not os.path.exists(dirs):
            os.makedirs(dirs)
            log.info(f'Diretório criado: {dirs}')
    except BaseException as err:
        log.error(f'Erro ao tentar criar diretório. {err}')
        raise CloseSpider('Ocorreu um erro ao tentar criar uma no diretório OUTPUT')


def slug(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
