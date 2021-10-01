# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

# Função para remover os espaços do início e do final da frase
def remove_quotations(value):
    return value.replace(u"\u201d", '').replace(u"\u201c", '')

class QuoteItem(scrapy.Item):
    text = scrapy.Field(
        input_processor = MapCompose(str.strip, remove_quotations), # Remove somente os espaços com a função remove_quotations e str.strip remove o "\n", utiliza o processador de entrada
        output_processor = TakeFirst() # Processador de saída
    )
    author = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip), # Utiliza uma função da biblioteca w3lib.html a remove_tags, str.strip remove o "\n"
        output_processor = TakeFirst()
    )
    tags = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Join(',')
    )
