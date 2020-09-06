# # -*- coding: utf-8 -*-
# import scrapy
# from real_estate_scrapper.items import Estate
# from real_estate_scrapper.itemLoaders import MojikvadratiEstateLoader
# import datetime
# import csv
# import json
# from scrapy.http import HtmlResponse
#
#
# now=datetime.datetime.now()
# old_estates_path = "scraped_data/mojikvadrati.csv"
#
# post_headers = {
# "Host":"mojikvadrati.com",
# "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",
# "Accept":"application/json, text/javascript, */*; q=0.01",
# "Accept-Language":"en-US,en;q=0.5",
# "Accept-Encoding":"gzip, deflate, br",
# "Referer":"https://mojikvadrati.com/nepremicnine",
# "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
# "X-Requested-With":"XMLHttpRequest",
# "Content-Length":"{0}",
# "Connection":"keep-alive"
# }
#
# #post_body = "property_type=5&price=50000-135000&location%5B%5D=13%3A%3A0%3A%3A0&offer_type=1&save_criteria=0&filter_name=&criteria_id=&search=1&option=advanced&options=%7B%7D&order=%3Fsort%3Dcreated_lt-desc&filter=default&items_list_variation=default&per_page_tracker={0}&page={1}"
# post_body = "offer_type=1&location%5B%5D=13%3A%3A0%3A%3A0&property_type=5&size=40-500&price=50000-135000&save_criteria=0&filter_name=&criteria_id=&search=1&option=advanced&options=%7B%7D&order=%3Fsort%3Dcreated_lt-desc&filter=default&items_list_variation=default&per_page_tracker={0}&page={1}"
#
# def get_old_urls(path):
#     links = []
#     try:
#         with open(path, 'r') as infile:
#             reader = csv.DictReader(infile)
#             for line in reader:
#                 links.append(line['url'])
#     except:
#         pass
#     return links
#
#
# old_urls = get_old_urls(old_estates_path)
#
# #mojikvadrati_filter_cookie = {'filter' : '%7B%22offer_type%22%3A%221%22%2C%22property_type%22%3A%225%22%2C%22size%22%3A%2243-500%22%2C%22price%22%3A%220-135000%22%2C%22location%22%3A%5B%2213%3A%3A0%3A%3A0%22%5D%2C%22search%22%3A%221%22%2C%22option%22%3A%22advanced%22%2C%22per_page_tracker%22%3A%22-1%22%7D'}
#
# class MojikvadratiSpider(scrapy.Spider):
#     name = 'mojikvadrati'
#     allowed_domains = ['mojikvadrati.com']
#     start_urls = ['https://mojikvadrati.com/nepremicnine']
#
#     def parse(self, response):
#         if (response.request.method != "POST"):
#             print("Initializing first post")
#             current_page = 1
#             per_page = 0
#             body = post_body.format(per_page, current_page)
#             headers = post_headers.copy()
#             headers['Content-Length'] = headers['Content-Length'].format(len(body))
#             yield scrapy.Request("https://mojikvadrati.com/engine/call/project_model/ajax_get_items_list",method='POST', body=body, headers=headers, callback=self.parse)
#         else:
#             html = HtmlResponse(url="Local", body = json.loads(response.text)['result']['html'], encoding='utf-8')
#             links = list(set(html.xpath('//a[contains(@href, "moji")]/@href').extract()))
#             #links = list(set([link.replace("\\","").replace('"','') for link in response.xpath('//a/@href').extract() if "nepremicnina" in link]))
#             for link in links:
#                 if link not in old_urls:
#                     print("Following link: " + link)
#                     if link != "https://mojikvadrati.com":
#                         yield scrapy.Request(link, callback=self.parse_estate_data,dont_filter=True)
#             if ("Trenutno na trgu ni" not in response.text ):
#                 per_page = int(str(response.request.body).split("=")[-2].split("&")[0]) + 15
#                 current_page = int(str(response.request.body).split("=")[-1].replace("'","").replace('"','')) + 1
#                 body = post_body.format(per_page, current_page)
#                 headers = post_headers.copy()
#                 headers['Content-Length'] = headers['Content-Length'].format(len(body))
#                 print("Going on to page: " + str(current_page))
#                 yield scrapy.Request("https://mojikvadrati.com/engine/call/project_model/ajax_get_items_list",method='POST', body=body, headers=headers, callback=self.parse)
#
#     def parse_estate_data(self,response):
#         print("On estate page")
#         loader = MojikvadratiEstateLoader(item = Estate(), response = response)
#         loader.add_xpath('price', '//div[@class="detail-cost-label green"]/text()')
#         loader.add_xpath('location', '//div[@class="container"]//h1/text()')
#         loader.add_xpath('size', '//span[contains(text(),"Velikost")]/../strong/text()')
#         loader.add_xpath('floor', '//span[contains(text(),"Nadstropje")]/../strong/text()')
#         loader.add_xpath('built', '//span[contains(text(),"Zgrajeno")]/../strong/text()')
#         loader.add_xpath('text', '//div[@id="description-section"]')
#         loader.add_value('url', response.request.url)
#         loader.add_value('parsed', now.strftime("%d.%m.%Y "))
#         print("Getting data")
#         return loader.load_item()
