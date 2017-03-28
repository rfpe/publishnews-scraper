# -*- coding: utf-8 -*-

import scrapy
import scrapy.http.request
from publishnews.items import Livro


class PnSemanalSpider(scrapy.Spider):
    name = "pn-semanal"
    start_urls = ["http://www.publishnews.com.br/ranking"]

    def parse(self, response):
        week_links = response.xpath('//*[@id="pn-selecao-semanal"]/div/a/@href').extract()

        for link in week_links:
            # Formato do link: "/ranking/semanal/0/2017/3/24/0/0"
            data_referencia = link.split("/")[4] + "-" + link.split("/")[5] + "-" + link.split("/")[6]

            yield scrapy.Request(callback=self.parse_book_ranking,
                                 url="http://www.publishnews.com.br" + link,
                                 meta={"data_referencia": data_referencia})

    def parse_book_ranking(self, response):

        livro_divs = response.xpath('//*/div[@class="pn-ranking-livros-corpo clearfix"]/div')

        for livro_div in livro_divs:

            l = Livro()

            # Atributos do ranking
            l['posicao_ranking'] = livro_div.xpath('./div[1]/text()').extract_first()
            l['volume_compra'] = livro_div.xpath('./div[2]/text()').extract_first().replace('.', '')

            # Atributos presentes no cabecalho
            cabecalho_livro = livro_div.xpath('./div[3]/div[1]/div[1]')
            l['titulo'] = cabecalho_livro.xpath('./div[2]/text()').extract_first()
            l['autor'] = cabecalho_livro.xpath('./div[3]/text()').extract_first()
            l['editora'] = cabecalho_livro.xpath('./div[4]/text()').extract_first()

            # Atributos presentes na div oculta
            dados_extras = livro_div.xpath('./div[3]/div[1]/div[2]/div')

            for item_extra in dados_extras:

                item_label = item_extra.xpath('./text()').extract_first()

                if item_label is not None:

                    item_label = item_label.strip().lower()
                    item_value = item_extra.xpath('./strong/text()').extract_first()

                    if item_label == "tradução":
                        l['tradutores'] = item_value
                    elif item_label == "isbn":
                        l['isbn'] = item_value.replace('-', '')
                    elif item_label == "categoria":
                        l['categoria'] = item_value
                    elif item_label == "preço":
                        l['preco'] = item_value.replace('R$ ', '').replace(',', '.')
                    elif item_label == "páginas":
                        l['numero_paginas'] = item_value
                    else:
                        # Não é possível fazer parsing
                        l['junk'] = item_extra.xpath('./strong/text()').extract_first()

            l['data_referencia'] = response.meta['data_referencia']

            yield l
