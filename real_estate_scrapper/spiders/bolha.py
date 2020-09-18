# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from real_estate_scrapper.items import Estate
from real_estate_scrapper.itemLoaders import EstateLoader
import datetime
import csv

now = datetime.datetime.now()
pages_limit = "10"

class BolhaSpider(scrapy.Spider):
    name = 'bolha'
    allowed_domains = ['www.bolha.com']
    start_urls = [
        'http://www.bolha.com/nepremicnine/stanovanja/?location=Osrednjeslovenska%2FLjubljana%2F&viewType=30&priceSortField=50000%7C135000&adTypeH=00_Prodam%2F&reSize=43|295']

    def __init__(self, url = None, scrape_file = None, *args, **kwargs):
        super(BolhaSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.scrape_file = scrape_file

    def parse(self, response):
        ads = response.xpath('//div[contains(@class, "EntityList--Regular")]//li[contains(@class, "EntityList-item")]')
        for ad in ads:
            url = response.urljoin(ad.xpath('.//a/@href').extract_first())
            yield Request(url, callback=self.parse_estate)
        next_page = response.xpath('//li[contains(@class, "Pagination-item--next")]/button/@data-page').extract_first()
        if next_page == pages_limit:
            return
        if next_page:
            yield response.follow(response.urljoin("?page=")+next_page)

    def parse_estate(self, response):
        loader = EstateLoader(item=Estate(), response=response)
        loader.add_value('page', self.name)
        loader.add_value('capture_date', now.isoformat())
        loader.add_value('location', str(response.xpath('//table[contains(@class, "table-summary")]//tr/th[contains(text(),"Lokacija")]/..//td/text()').extract_first()))

        price = response.xpath('//strong[contains(@class, "price")]/text()').extract_first().strip().replace(".", "")
        if "po dogovoru" in price:
            price = "-1"
        loader.add_value('price', str(price))

        size = response.xpath('//table[contains(@class, "table-summary")]//tr/th[contains(text(),"površina")]/..//td/text()').extract_first()
        if size is None:
            size = "999"
        size = size.replace("m²", "").replace(",", ".").strip()
        loader.add_value('size', str(size))
        loader.add_xpath('floor', '//table[contains(@class, "table-summary")]//tr/th[contains(text(),"Nadstropje")]/..//td/text()')
        loader.add_xpath('built', '//table[contains(@class, "table-summary")]//tr/th[contains(text(),"Leto izgradnje")]/..//td/text()')
        loader.add_xpath('text', '//div[contains(@class, "passage-standard")]//text()')
        loader.add_value('url', response.url)
        return loader.load_item()
