# -*- coding: utf-8 -*-

import scrapy

class Livro(scrapy.Item):
    titulo = scrapy.Field()
    data_referencia = scrapy.Field()
    posicao_ranking = scrapy.Field()
    autor = scrapy.Field()
    editora = scrapy.Field()
    isbn = scrapy.Field()
    categoria = scrapy.Field()
    preco = scrapy.Field()
    numero_paginas = scrapy.Field()
    volume_compra = scrapy.Field()
    tradutores = scrapy.Field()

    junk = scrapy.Field()
