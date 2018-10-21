#/bin/python3

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from apartment import Apartment

search_url = "/oglasi-prodaja/ljubljana-mesto/ljubljana-bezigrad,ljubljana-center,ljubljana-siska,ljubljana-vic-rudnik/stanovanje/cena-od-50000-do-150000-eur,velikost-od-43-do-100-m2,letnik-od-1943/"

base_url = "https://www.nepremicnine.net"

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
            links.append(base_url + add.a["href"])
        estates = get_url(url + str(i) + "/")
        html = BeautifulSoup(estates, "html.parser")
    return links


def get_apartments(links):
    apartments = []
    for link in links:
        apartments.append(get_apartment(link))
    return apartments

def get_apartment(link):
    estate = get_url(link)
    html = BeautifulSoup(estate, "html.parser")
   
    price = html.find("div", class_="cena").span.text.replace(".","").replace(",",".").split(" ")[1]
    description = html.find("div", class_="kratek")
    location = description.strong.text
    data = str(description).split(",")
    size = -1
    built = -1
    renewed = -1
    floor = -1
    
    for i in range(0,len(data)):
        if "m2" in data[i] and size == -1:
            if data[i-1].strip()[-1].isdigit():
                size = data[i-1] + "." +  data[i].replace("m2", "")
            else:
                size = data[i].replace("m2", "")
        if "zgrajeno" in data[i] and built == -1:
            built = data[i].replace("zgrajeno l.", "")
        if "adaptirano" in data[i] and renewed == -1:
            renewed = data[i].replace("adaptirano l.", "")
        if "nad" in data[i] and floor == -1:
            floor = data[i].replace("nad.","")
    return Apartment(link ,price, size, location,floor, built, renewed)


links = get_adds_urls(base_url,search_url)
apartments = get_apartments(links[:3])
for apartment in apartments[:3]:
    print(apartment)
