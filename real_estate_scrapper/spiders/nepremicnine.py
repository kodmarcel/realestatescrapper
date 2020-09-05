# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from real_estate_scrapper.items import Estate
from real_estate_scrapper.itemLoaders import EstateLoader
import datetime


now = datetime.datetime.now()

bad_classes = ["ogIasi","oġlasi","oglas¡","oglàsi","oglási","oglasì","ąds","àds","áds","äds","adś","adş"]

visit_url = "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/cena-od-50000-do-135000-eur,velikost-od-40-m2/"
andreja_url = "https://www.nepremicnine.net/oglasi-oddaja/ljubljana-mesto/stanovanje/cena-do-450-eur-na-mesec/"

class NepremicnineSpider(scrapy.Spider):
    name = 'nepremicnine'
    allowed_domains = ['nepremicnine.net']

    def __init__(self, url = None, scrape_file = None, *args, **kwargs):
        super(NepremicnineSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.scrape_file = scrape_file

    def parse(self, response):
        estates = response.xpath('//div[contains(@class, "oglas_container")]') # poberemo vse oglase na strani
        for estate in estates:
            estate_class = estate.xpath('@class').extract_first()
            if any([bad_class in estate_class for bad_class in bad_classes]): # pogledamo ce ima oglas katerega od slabih classov -> pomeni da ne pase v naso kategorijo
                continue
            relative_url = estate.xpath('.//a/@href').extract_first()

            loader = EstateLoader(item = Estate(), selector = estate)
            loader.add_value('page', self.name)
            loader.add_value('capture_date', now.isoformat())
            loader.add_xpath('location', './/span[@class="title"]/text()')
            loader.add_xpath('price', './/span[@class="cena"]/text()')
            loader.add_xpath('size', './/span[@class="velikost"]/text()')
            loader.add_xpath('built', './/span[@class="atribut leto"]/strong/text()')
            loader.add_xpath('floor', './/span[@class="atribut"]/strong/text()')
            loader.add_value('url', response.urljoin(relative_url))
            yield Request(response.urljoin(relative_url), cb_kwargs={'loader': loader}, callback = self.parse_text)
        next_page_url = response.urljoin(response.xpath('//a[@class="next"]/@href').extract_first())
        if next_page_url:
            yield Request(next_page_url, callback=self.parse)

    def parse_text(self, response, loader):
        text = response.xpath('//div[@id="opis"]').extract_first().split('<div class="spacer">')[0]
        loader.add_value('text', text)
        return loader.load_item()
