# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import geocoder
from itertools import combinations
import logging

logging.getLogger('geocoder.base').setLevel(logging.ERROR)
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

#Desired locaons
kongresni_location = geocoder.osm("Kongresni trg")
center = kongresni_location
country = "Slovenija"
city = "Ljubljana"


#Grading variables
price_factor = -2.5/1000 # so that 1000€ less means 2.5 points more
size_factor = 2.5 
per_meter_factor = -2/1000 # so that 1000€ less means 2.5 points more


save_file = "scraped_data/estates.json"

class EstateGradingPipeline(object):

        
    def process_item(self, item, spider):
        location = self.find_location(item['location'][0])
        item['distance'] = self.get_distance(location, center)
        item['points'] =self.grade_estate(item)
        return item

    def grade_estate(self,item):
        points = 216
        price_points = item['price']*price_factor
        size_points = item['size']*size_factor
        per_meter_poitns = item['price']/item['size']*per_meter_factor
        built_points = item['built']-1964
        renewed_points = (item['built']-1990)/4
        distance_points = 80/item['distance']**(1/1.1)        
        floor = item['floor']
        floor_points = 20
        if floor == 'P':
            floor_points = 0
        elif floor == 'M':
            floor_points = 10
        return points + price_points + size_points + per_meter_poitns + built_points + renewed_points + distance_points + floor_points 
    
    def find_location(self,location):
        loc = geocoder.osm(location)
        if loc.country !=country:
            locations = (location + ", " + city).replace(".", ",").split(",")
            for r in range(len(locations), 0, -1):
                possible = combinations(locations,r)
                for p in possible:
                    loc = geocoder.osm(",".join(p))
                    if loc.country == country:
                        return loc
        return loc

    def get_distance(self, location, center):
        if location.country == country:
            distance = geocoder.distance(center, location)
        else:
            distance = -1
        return distance

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open(save_file, 'w')
    
    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
