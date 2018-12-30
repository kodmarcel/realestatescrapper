# -*- coding: utf-8 -*-
import scrapy


class MojikvadratiSpider(scrapy.Spider):
    name = 'mojikvadrati'
    allowed_domains = ['mojikvadrati.com']
    start_urls = ['https://mojikvadrati.com/']

    def parse(self, response):
        print(response)
        pass
