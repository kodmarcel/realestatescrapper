# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from real_estate_scrapper.items import Estate
from real_estate_scrapper.itemLoaders import NepremicnineEstateLoader
import datetime
import csv

now = datetime.datetime.now()
old_estates_path = "scraped_data/bolha.csv"

def get_old_urls(path):
    links = []
    try:   
        with open(path, 'r') as infile:
            reader = csv.DictReader(infile)
            for line in reader:
                links.append(strip_url(line['url']))
    except:
        pass    
    return links

def strip_url(url):
    if 'bolha' in url:
        return url.split('.html')[0] + '.html'
    return url



old_urls = get_old_urls(old_estates_path)

class BolhaSpider(scrapy.Spider):
    name = 'bolha'
    allowed_domains = ['www.bolha.com']
    start_urls = ['http://www.bolha.com/nepremicnine/stanovanja/?location=Osrednjeslovenska%2FLjubljana%2F&viewType=30&priceSortField=50000%7C135000&adTypeH=00_Prodam%2F&reSize=43|295']

    def parse(self, response):
        ads = response.xpath('//div[@class="ad"]')
        for ad in ads:
            url = strip_url(response.urljoin(ad.xpath('.//a/@href').extract_first()))
            if url not in old_urls:
                yield Request(url, callback = self.parse_estate)
        follow_url = response.xpath('//a[@class="forward"]/@href').extract_first()
        if follow_url:
           yield response.follow(follow_url)

    def parse_estate(self, response):
        loader = NepremicnineEstateLoader(item = Estate(),response = response)
        loader.add_xpath('location', '//table[@class="oglas-podatki"]/tr/td[contains(text(),"naselje")]/..//b/text()')
        loader.add_xpath('price', '//div[@class="price"]/span/text()')
        loader.add_xpath('size', '//table[@class="oglas-podatki"]/tr/td[contains(text(),"Velikost")]/..//b/text()')
        loader.add_xpath('floor', '//table[@class="oglas-podatki"]/tr/td[contains(text(),"Nadstropje")]/..//b/text()')
        loader.add_xpath('built', '//table[@class="oglas-podatki"]/tr/td[contains(text(),"Leto izgradnje")]/..//b/text()')
        loader.add_value('url',response.url)
        loader.add_value('parsed', now.strftime("%d.%m.%Y "))
        return loader.load_item() 
