# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from real_estate_scrapper.items import Estate
from real_estate_scrapper.itemLoaders import EstateLoader
import datetime
import csv

now = datetime.datetime.now()

class BolhaSpider(scrapy.Spider):
    name = 'bolha'
    allowed_domains = ['www.bolha.com']

    def __init__(self, url = None, run_name = None, export_headers = True, *args, **kwargs):
        super(BolhaSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.run_name = run_name 
        self.export_headers = export_headers

    def parse(self, response, origin_url = None):
        ads = response.xpath('//div[contains(@class, "EntityList--Regular")]//li[contains(@class, "EntityList-item")]')
        for ad in ads:
            url = response.urljoin(ad.xpath('.//a/@href').extract_first())
            yield Request(url, callback=self.parse_estate)

        next_page = response.xpath('//li[contains(@class, "Pagination-item--next")]/button/@data-page').extract_first()
        if origin_url == None:
            origin_url = response.url
        if next_page:

            if "?" not in origin_url:
                origin_url + "?"
            yield response.follow(origin_url + "&page=" + next_page, cb_kwargs = {"origin_url": origin_url})

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
            size = "-1"
        size = size.replace("m²", "").replace(",", ".").strip()
        loader.add_value('size', str(size))
        loader.add_xpath('floor', '//table[contains(@class, "table-summary")]//tr/th[contains(text(),"Nadstropje")]/..//td/text()')
        loader.add_xpath('built', '//table[contains(@class, "table-summary")]//tr/th[contains(text(),"Leto izgradnje")]/..//td/text()')
        loader.add_xpath('text', '//div[contains(@class, "passage-standard")]//node()')
        loader.add_value('url', response.url)
        return loader.load_item()
