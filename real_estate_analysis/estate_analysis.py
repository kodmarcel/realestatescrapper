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
from datetime import datetime
import time

logging.getLogger('geocoder.base').setLevel(logging.ERROR)
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

#Scraped data location
project_folder = "/home/marcel/Projects/RealEstateScrapper/"
data_folder = project_folder + "scraped_data/"
estate_files = ["nepremicnine.csv", "mojikvadrati.csv", "bolha.csv"]

#Analyzed data lcoation
analyzed_data_folder = project_folder + "analyzed_data/"
analyzed_data_filename = "estates.csv"
output_path = analyzed_data_folder + analyzed_data_filename
readable_path = analyzed_data_folder + "estates.txt"


#Ignored estates location
ignored_path = project_folder + "ignored_estates"

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
header = ['points', 'price', 'size', 'psm', 'distance', 'floor', 'location','found_location', 'built' , 'renewed', 'parsed', 'url']

def get_ignored(path):
    with open(ignored_path,'r') as ignored:
        lines = ignored.readlines()
    for i in range(len(lines)):
        lines[i] = strip_url(lines[i].strip())
    return lines

def get_parsed_data(ignored_urls):
    estates = []
    for estate_file in estate_files:
        estate_file = data_folder + estate_file        
        with open(estate_file, 'r') as in_file:
            for estate in csv.DictReader(in_file):
                estate['url'] = strip_url(estate['url'])
                if estate['url'] in ignored_urls or 'oddaja' in estate['url']:
                    continue
                parse_estate(estate)
                estates.append(estate)
    return estates       

def strip_url(url):
    if 'bolha' in url:
        return url.split('.html?')[0] + '.html'
    return url


def parse_estate(estate):
    try:
        estate['price'] = float(estate['price'])
    except:
        estate['price'] = 110000
    try:
        estate['size'] = float(estate['size'])
    except:
        estate['size'] = 48
    try:
        estate['built'] = float(estate['built'])
    except:
        estate['built'] = 1970 
    if 'points' in estate.keys():
        estate['points'] = float(estate['points'])
    if 'distance' in estate.keys():
        estate['distance'] = float(estate['distance'])


def get_analyzed_data():
    estates = []
    try:
        with open(output_path, 'r') as in_file:
            for estate in csv.DictReader(in_file):
                parse_estate(estate)
                estates.append(estate)
    except:
        pass
    return estates       
        

def store_estates(estates, filename):
    #keys = estates[0].keys()
    with open(filename, "w") as out_file:
        #dict_writer = csv.DictWriter(out_file, keys)
        dict_writer = csv.DictWriter(out_file, header)
        dict_writer.writeheader()
        dict_writer.writerows(estates)

def store_readable(estates, output_file):
    with open(output_file, 'w') as output:
        for estate in estates:
            output.write(get_readable_form(estate))

def get_readable_form(estate):
    string = ""
    for head in header:
        string += head + ": "
        string += str(estate[head])
        string += "\n"
    string += "\n"
    return string

def sort_estates(estates, field):
    if field == "parsed":
        return sorted(estates, key= lambda estate: datetime.strptime(estate[field],'%d.%m.%Y '), reverse=True)
    return sorted(estates, key= lambda estate: estate[field], reverse=True)

def grade_estate(estate):
    points = 0 
    price_points = (130 - estate['price']/1000)*price_ratio / (130-70)
    size_points = estate['size'] - 43 * size_ratio /(90-43)
    built_points = max(0,(estate['built']-1964)*built_ratio/(2000-1964))
    distance_points = (6-estate['distance'])*distance_ratio/6
    floor = estate['floor']
    floor_points = 10
    if floor == 'M':
        floor_points = 5
    elif floor == 'VP':
        floor_points = 3.5
    elif floor == 'P' or floor == 'Pritličje':
        floor_points = 2.5 
    elif floor == 'PK' or floor == 'Polklet':
        floor_points = 0
    return points + price_points + size_points + built_points + distance_points + floor_points 

def find_location(location):
    locations = location.lower().replace("-", ",").replace("lj.", "ljubljana,").split(",")
    for location in locations:
        if location.find("lokac") != -1:
            locations.remove(location)
    location = ",".join(locations)
    loc = geocoder.osm(location)
    if not loc.ok or loc.city != city:
        loc = geocoder.osm(city + "," + locations[-1])
        if not loc.ok or loc.city != city:
            if len(locations) > 1:
                loc = geocoder.osm(city + "," + locations[-2])
            else:
                loc = geocoder.osm(city)
    return loc        


def get_distance(location, center):
    if location.country == country:
        distance = geocoder.distance(center, location)
    else:
        distance = -1
    return distance
#print('Getting saved data')
ignored_urls = get_ignored(ignored_path)
estates = get_parsed_data(ignored_urls)
old_estates = get_analyzed_data()
new = 0
new_estates = []
checked_estates = set()

now = time.time()
wait = 0.1 
duplicates = []
#print('Iterating over estates')
for estate in estates:
    found = False
    if estate['url'] in checked_estates:
        duplicates.append(estate)
        continue
    checked_estates.add(estate['url'])
    for old_estate in old_estates:
        if estate['url'] == old_estate['url'] and estate['location'] == old_estate['location'] and estate['price'] == old_estate['price']:
            estate['found_location'] = old_estate['found_location']
            estate['distance'] = old_estate['distance']
            estate['parsed'] = old_estate['parsed']
            old_estates.remove(old_estate)
            found = True
            break
    if not found:
        #print('Found new estate: ' + estate['url'])
        if time.time() - now < wait:
            time.sleep(wait) 
        new += 1
        new_estates.append(estate)
        location = estate['location']
        found_location = find_location(location)
        estate['found_location'] = found_location.address
        distance = get_distance(found_location, center)
        estate['distance'] = distance
        now = time.time()
    points = grade_estate(estate)
    estate['points'] = points 
    estate['psm'] = estate['price']/estate['size']

#delete duplicates
for duplicate in duplicates:
    estates.remove(duplicate)

#print("Sorting estates")
estates = sort_estates(estates, 'points')
new_estates = sort_estates(new_estates, 'points')

#print("Saving data")
store_estates(estates, output_path)
store_readable(estates, readable_path)

#print("RESULTS")
#newest_estates = sort_estates(estates, 'parsed')[:10]
print("{} new estates: ".format(new))
for estate in new_estates:
    print(get_readable_form(estate))

print()
amount = 20

print("{} best estates: ".format(amount))
for estate in estates[:amount]:
    print(get_readable_form(estate))

