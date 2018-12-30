#/bin/python3

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from apartment import Apartment
from apartment_json import ApartmentsEncoder
from apartment_json import ApartmentsDecoder
import googlemaps
from datetime import datetime
import json
import geocoder
from itertools import combinations
import datetime

now = datetime.datetime.now()

search_url = "/oglasi-prodaja/ljubljana-mesto/ljubljana-bezigrad,ljubljana-center,ljubljana-siska,ljubljana-vic-rudnik/stanovanje/1.5-sobno,2-sobno,2.5-sobno,3-sobno,3.5-sobno,4-sobno/cena-od-50000-do-130000-eur,velikost-od-43-do-100-m2,letnik-od-1943/"

base_url = "https://www.nepremicnine.net"

bad_classes = ["ogIasi","oġlasi","oglas¡","oglàsi","oglási","oglasì","ąds","àds","áds","äds","adś","adş"]

apartmetns_file = "apartments.json"
links_file = "links.json"
ignore_links_file="ignore_links"
apartments_representation_file = "apartments_for_reading.txt"

kongresni_location = geocoder.osm("Kongresni trg")

def get_url(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_response_valid(resp):
                return resp.content
            else:
                log_error("Invalid response")
                return None
    except RequestException as e:
        log_error("Error during request to {0} : {1}".format(url, str(e)))
        return None

def get_page_count(html):
    adds_count = int(html.find(attrs={"class": "oglasi_cnt"}).strong.text)
    adds_per_page = len(html.find_all("div", class_="oglas_container"))
    count = adds_count // adds_per_page + 1
    return count

def is_response_valid(resp):
   content_type = resp.headers["Content-Type"].lower()
   return (resp.status_code == 200 and content_type is not None and content_type.find("html") > -1)

def log_error(e):
    print(e)

def get_adds_urls(base_url, search_url):
    url = base_url + search_url
    links = []
    estates = get_url(url)
    html = BeautifulSoup(estates, "html.parser")

    pages = get_page_count(html)

    for i in range(2, pages + 2):
        adds = html.find_all("div", class_="oglas_container")
        for add in adds:
            if "prodaja" in add.a["href"]:
                skip = False
                for bad in bad_classes:
                    for cl in add["class"]:
                        if bad in cl:
                            skip = True
                            break
                    if skip:
                        break
                if skip:
                    continue
                links.append(base_url + add.a["href"])
        estates = get_url(url + str(i) + "/")
        html = BeautifulSoup(estates, "html.parser")
    return links


def get_apartments(links):
    apartments = []
    for link in links:
        try:
            apartments.append(get_apartment(link))
        except:
            print("Cant get info from : " + link)
            continue
    return apartments

def find_location(location):
    loc = geocoder.osm(location)
    if loc.country != "Slovenija":
        locations = (location + ", ljubljana").replace(".", ",").split(",")
        for r in range(len(locations), 0, -1):
            possible = combinations(locations,r)
            for p in possible:
                loc = geocoder.osm(",".join(p))
                if loc.country == "Slovenija":
                    return loc
    return loc


def get_apartment(link):
    try:
        estate = get_url(link)
        html = BeautifulSoup(estate, "html.parser")
    except:
        print("Link not OK: " + link )
        return None

    price = html.find("div", class_="cena").span.text.replace(".","").replace(",",".").split("€")[0]
    price = "".join(filter(lambda x: x in '.0123456789', price))
    description = html.find("div", class_="kratek")
    location = description.strong.text.lower()
    data = str(description).split(",")
    size = -1
    built = -1
    renewed = -1
    floor = -1

    loc = find_location(location)
    if loc.country == 'Slovenija':
        distance = geocoder.distance(kongresni_location, loc)
    else:
        distance = -1

    for i in range(0,len(data)):
        if "m2" in data[i] and size == -1:
            if data[i-1].strip()[-1].isdigit():
                size = data[i-1] + "." +  data[i].replace("m2", "")
            else:
                size = data[i].replace("m2", "")
        if "zgrajeno" in data[i] and built == -1:
            built = "".join(filter(lambda x: x in '0123456789', data[i]))
        if "adaptirano" in data[i] and renewed == -1:
            renewed = "".join(filter(lambda x: x in '0123456789', data[i]))
        if "nad" in data[i] and floor == -1:
            floor = data[i].replace("nad.","")
    return Apartment(link ,price, size, location,floor, built, renewed, distance)

def sort_apartments(apartments):
    return sorted(apartments, key=lambda x:x.points, reverse=True)

def save_apartments(apartments, file):
    with open(file, "w") as outfile:
        json.dump(apartments, outfile, cls=ApartmentsEncoder)

def load_apartments(file):
    try:
        with open(file, "r") as infile:
            data = json.load(infile, object_hook=ApartmentsDecoder.object_hook)
        return data
    except:
        return []


def load_links(file):
    try:
        with open(links_file, "r") as infile:
            links = json.load(infile)
        return links
    except:
        return []

def get_ignore_links(infile):
    with open(infile,"r") as infile:
        links = infile.read().split("\n");
    return links


#print("Loading links from file...")
links = load_links(links_file)

ignore_links = get_ignore_links(ignore_links_file)

#print("Getting new links to apartments from web...")
current_links = get_adds_urls(base_url,search_url)

current_links = list(set(current_links) - set(ignore_links))

new_links = list(set(current_links) - set(links))

links = current_links


#print("Deleting apartments that should be ignored")


#print("Loading apartments from file...")
apartments = load_apartments(apartmetns_file)
#print("Getting new apartments data from web ...")
new_apartments = get_apartments(new_links)

apartments = list(set(apartments) | set(new_apartments))

#print("Calculating apartments points and deleting them if supposed to ignore")
for apartment in apartments:
    if apartment == None or apartment.link in ignore_links:
        apartments.remove(apartment)
        continue
    apartment.calculate_points()

#print("Deleting apartments that should be ignored")

#print("Sorting apartments ...")
apartments = sort_apartments(apartments)
new_apartments = sort_apartments(new_apartments)


#print("Saving deleting outdated links and apartment...")
for apartment in apartments:
    if apartment.link not in links:
        apartments.remove(apartment)

#print("Saving links...")
with open(links_file, "w") as outfile:
    json.dump(links, outfile)

#print("Saving apartments...")
save_apartments(apartments, apartmetns_file)
with open(apartments_representation_file, 'w') as infile:
    infile.write("Report on the day " + now.strftime("%d.%m.%Y") + ":\n")
    infile.write("Got {} hits".format(len(links)) + "\n")
    infile.write("\n")
    for apartment in apartments:
        infile.write("\n")
        infile.write(str(apartment))
        infile.write("\n")

print()
print("Changes from last run:\n")
for apartment in new_apartments:
    print()
    print(apartment)


print()
print()
print("Displaying best 5 apartments:\n")
for apartment in apartments[:5]:
    print()
    print(apartment)
