from run import main

name = "example_rent"
scrap_urls = ["https://www.nepremicnine.net/oglasi-oddaja/ljubljana-mesto/stanovanje/cena-do-450-eur-na-mesec/"]
distance_from = "Kongresni trg, Ljubljana, Slovenija"
ignore_list = ["brez_postelje"]
scrape_file = "scraped_data/" + name + ".csv"
archive_data_file = "archive_data/" + name + ".csv"
print_columns = ["points", "location", "price", "size", "distance", "new", "url"]


def calculate_points(estate):
    if estate['size'] < 38:
        size_points = 0
    elif estate['size'] < 45:
        size_points = 30
    elif estate['size'] < 50:
        size_points = 60
    elif estate['size'] < 55:
        size_points = 70
    elif estate['size'] < 60:
        size_points = 80
    else:
        size_points = 100
    if estate['distance'] < 1:
        distance_points = 70
    elif estate['distance'] < 2:
        distance_points = 100
    elif estate['distance'] < 3:
        distance_points = 80
    elif estate['distance'] < 4:
        distance_points = 60
    elif estate['distance'] < 5:
        distance_points = 40
    else:
        distance_points = 20

    return size_points + distance_points

main(name, scrap_urls, ignore_list, calculate_points, distance_from,scrape_file, archive_data_file, print_columns )
