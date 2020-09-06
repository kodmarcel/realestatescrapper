from run import main

name = "example_rent"
scrap_urls = ["https://www.nepremicnine.net/oglasi-oddaja/ljubljana-mesto/stanovanje/cena-do-450-eur-na-mesec/"]
distance_from = "Kongresni trg, Ljubljana, Slovenija"
ignore_list = ["oddamo sob","oddam sob","oddaja se sob", "oddajam sobo", "študentsko sobo", "oddaja se postelj","oddaja postelj","oddamo postelj", "oddamo dvoposteljno", "souporab","delit", "skupno", "že stanuje", "oddamo posteljo", "postelji oddamo", "https://www.nepremicnine.net/oglasi-oddaja/lj-siska-stanovanje_6360581/", "https://www.nepremicnine.net/oglasi-oddaja/jezica-bezigrad-ruski-car-stanovanje_6359280/", "https://www.nepremicnine.net/oglasi-oddaja/lj-vic-sibeniska-ulica-5-stanovanje_6309122/", "https://www.nepremicnine.net/oglasi-oddaja/lj-vic-rozna-dolina-stanovanje_6203756/", "https://www.nepremicnine.net/oglasi-oddaja/lj-moste-stanovanje_6323521/","https://www.nepremicnine.net/oglasi-oddaja/lj-vic-stanovanje_6359292/"]
scrape_file = "scraped_data/" + name + ".csv"
archive_data_file = "archive_data/" + name + ".csv"
print_columns = ["points", "location", "price", "size", "distance", "new", "url"]


def calculate_points(estate):
    if not estate["active"]:
        return 0
    if estate['size'] < 10:
        size_points = 0
    elif estate['size'] < 20:
        size_points = 30
    elif estate['size'] < 30:
        size_points = 60
    elif estate['size'] < 50:
        size_points = 70
    elif estate['size'] < 60:
        size_points = 80
    else:
        size_points = 0

    if estate["price"] < 100:
        price_points = 10
    elif estate["price"] < 150:
        price_points = 100
    elif estate["price"] < 200:
        price_points = 80
    elif estate["price"] < 250:
        price_points = 60
    elif estate["price"] < 300:
        price_points = 40
    elif estate["price"] < 350:
        price_points = 20
    elif estate["price"] < 400:
        price_points = 10
    else:
        price_points = 0

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
        distance_points = 0

    return size_points + distance_points + price_points

main(name, scrap_urls, ignore_list, calculate_points, distance_from,scrape_file, archive_data_file, print_columns )
