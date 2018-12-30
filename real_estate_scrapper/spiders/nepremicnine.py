# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from real_estate_scrapper.items import Estate
from real_estate_scrapper.itemLoaders import NepremicnineEstateLoader
import datetime

now = datetime.datetime.now()

class NepremicnineSpider(scrapy.Spider):
    name = 'nepremicnine'
    allowed_domains = ['nepremicnine.net']
    start_urls = ["https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/cena-od-50000-do-135000-eur/"]

    def parse(self, response):
        for estate in self.parse_estate_listing(response):
            yield estate 

    def parse_estate_listing(self, response):
        estates = response.xpath('//div[contains(@class, "oglas_container")]')
        for estate in estates:
            loader = NepremicnineEstateLoader(item = Estate(), selector = estate)
            loader.add_xpath('location', './/span[@class="title"]/text()')
            loader.add_xpath('price', './/span[@class="cena"]/text()')
            loader.add_xpath('size', './/span[@class="velikost"]/text()')
            loader.add_xpath('built', './/span[@class="atribut leto"]/strong/text()')
            loader.add_xpath('floor', './/span[@class="atribut"]/strong/text()')
            relative_url = estate.xpath('.//a/@href').extract_first()
            loader.add_value('url', response.urljoin(relative_url))
            loader.add_value('parsed', now.strftime("%d.%m.%Y "))
            yield loader.load_item()
        next_page_url = response.urljoin(response.xpath('//a[@class="next"]/@href').extract_first())
        if next_page_url:
            yield Request(next_page_url, callback=self.parse_estate_listing)
