# -*- coding: utf-8 -*-

# Define your estate pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/estate-pipeline.html

import json
import geocoder
from itertools import combinations
import logging
import csv

logging.getLogger('geocoder.base').setLevel(logging.ERROR)
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

#Scraped data location
project_folder = "/home/marcel/Projects/RealEstateScrapper/"
data_folder = project_folder + "scraped_data/"
estate_files = ["nepremicnine.csv"]

#Analyzed data lcoation
analyzed_data_folder = project_folder + "/analyzed_data/"
analyzed_data_filename = "estates.csv"
output_path = analyzed_data_folder + analyzed_data_filename

#Desiredi estate locations
kongresni_location = geocoder.osm("Kongresni trg")
center = kongresni_location
country = "Slovenija"
city = "Ljubljana"


#Grading ratios
size_ratio = 40
distance_ratio = 25
price_ratio = 20
floor_ratio = 10
built_ratio = 5

#Desired output
header = ['points', 'price', 'size', 'psm', 'distance', 'floor', 'location','found_location', 'built' , 'renewed', 'url']

def get_parsed_data():
    estates = []
    for estate_file in estate_files:
        estate_file = data_folder + estate_file        
        with open(estate_file, 'r') as in_file:
            for estate in csv.DictReader(in_file):
                estates.append(estate)
    return estates       
        
def get_analyzed_data():
    estates = []
    with open(output_path, 'r') as in_file:
        for estate in csv.DictReader(in_file):
            estates.append(estate)
    return estates       
        

def store_estates(estates, filename):
    #keys = estates[0].keys()
    with open(filename, "w") as out_file:
        #dict_writer = csv.DictWriter(out_file, keys)
        dict_writer = csv.DictWriter(out_file, header)
        dict_writer.writeheader()
        dict_writer.writerows(estates)

def sort_estates(estates, field):
    return sorted(estates, key= lambda estate: estate[field], reverse=True)

def grade_estate(estate):
    points = 0 
    price_points = (130 - float(estate['price'])/1000)*price_ratio / (130-70)
    size_points = float(estate['size']) - 43
    built_points = (float(estate['built'])-1964)*5/(2000-1964)
    distance_points = (6-float(estate['distance']))*distance_ratio/6
    floor = estate['floor']
    floor_points = 10
    if floor == 'M':
        floor_points = 5
    elif floor == 'VP':
        floor_points = 3.5
    elif floor == 'P':
        floor_points = 2.5 
    elif floor == 'PK':
        floor_points = 0
    return points + price_points + size_points + built_points + distance_points + floor_points 

def find_location(location):
    location = location + ", " + city
    loc = geocoder.osm(location)
    if loc.country !=country:
        locations = location.replace(".", ",").split(",")
        for r in range(len(locations), 0, -1):
            possible = combinations(locations,r)
            for p in possible:
                loc = geocoder.osm(",".join(p))
                if loc.country == country:
                    return loc
    return loc

def get_distance(location, center):
    if location.country == country:
        distance = geocoder.distance(center, location)
    else:
        distance = -1
    return distance

estates = get_parsed_data()
estate = estates[0]
for estate in estates:
    estate['psm'] = float(estate['price'])/float(estate['size'])
    location = estate['location']
    found_location = find_location(location)
    estate['found_location'] = found_location.address
    distance = get_distance(found_location, center)
    estate['distance'] = distance
    points = grade_estate(estate)
    estate['points'] = points 

estates = sort_estates(estates, 'points')

store_estates(estates, output_path)

