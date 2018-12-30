# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import geocoder
from itertools import combinations

kongresni_location = geocoder.osm("Kongresni trg")
country = "Slovenija"
ciry = "Ljubljana"

class RealEstateScrapperPipeline(object):
    def process_item(self, item, spider):
        return item

class EstatesPipeline(object):


    def process_item(self, item, spider):
       location = item['location'] 
       distance = getDistance(location, kongresni_location)



    def find_location(location):
        loc = geocoder.osm(location)
        if loc.country !=i country:
            locations = (location + ", " + city).replace(".", ",").split(",")
            for r in range(len(locations), 0, -1):
                possible = combinations(locations,r)
                for p in possible:
                    loc = geocoder.osm(",".join(p))
                    if loc.country == country:
                        return loc
        return loc

    def getDistance(location, center):
        if loc.country == 'Slovenija':
            distance = geocoder.distance(kongresni_location, loc)
        else:
            distance = -1


