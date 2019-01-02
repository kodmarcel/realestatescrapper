# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from real_estate_scrapper.items import Estate
from real_estate_scrapper.itemLoaders import NepremicnineEstateLoader
import datetime

now = datetime.datetime.now()
old_estates_path = "scraped_data/nepremicnine.csv"

def get_old_urls(path):
    links = []
    try:   
        with open(path, 'r') as infile:
            reader = csv.DictReader(infile)
            for line in reader:
                links.append(line['url'])
    except:
        pass    
    return links


old_urls = get_old_urls(old_estates_path)

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
            relative_url = estate.xpath('.//a/@href').extract_first()
            if response.urljoin(relative_url) in old_urls:
                continue
            loader = NepremicnineEstateLoader(item = Estate(), selector = estate)
            loader.add_xpath('location', './/span[@class="title"]/text()')
            loader.add_xpath('price', './/span[@class="cena"]/text()')
            loader.add_xpath('size', './/span[@class="velikost"]/text()')
            loader.add_xpath('built', './/span[@class="atribut leto"]/strong/text()')
            loader.add_xpath('floor', './/span[@class="atribut"]/strong/text()')
            loader.add_value('url', response.urljoin(relative_url))
            loader.add_value('parsed', now.strftime("%d.%m.%Y "))
            yield loader.load_item()
        next_page_url = response.urljoin(response.xpath('//a[@class="next"]/@href').extract_first())
        if next_page_url:
            yield Request(next_page_url, callback=self.parse_estate_listing)
