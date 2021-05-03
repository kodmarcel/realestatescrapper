from run import main, analyze_data

name = "example_buy_sandra"
scrap_urls = ["https://www.nepremicnine.net/oglasi-prodaja/gorenjska/cena-do-200000-eur,velikost-od-70-m2/","https://www.bolha.com/prodaja-stanovanja/gorenjska?price%5Bmax%5D=200000&livingArea%5Bmin%5D=70&numberOfRooms%5Bmin%5D=two-rooms&typeOfTransaction=sell","https://www.bolha.com/prodaja-hise/gorenjska?price%5Bmax%5D=200000&livingArea%5Bmin%5D=70&typeOfTransaction=sell"]
distance_from = None
ignore_list = ["Jesenice","Kropa","poslovni",
"https://www.bolha.com/nepremicnine/prodaja-hisa-samostojna-gorenjska-kranjska-gora-mojstrana-oglas-6477762"]
scrape_file = "scraped_data/" + name + ".csv"
archive_data_file = "archive_data/" + name + ".csv"
print_columns = ["points", "location", "price", "size", "distance", "captured_today", "url"]


scoring_map = {
    "price": [{
        "type": "reverse",
        "points_per_unit": 1
    },],
    "built": {
        "type": "normal",
        "points_per_unit": 500
    },
    "size": {
        "type": "normal",
        "points_per_unit": 2000,
    },
    "floor": {
        "type": "contains",
        "values": ["PK"],
        "points": -20000
    },
    "active": {
        "type": "cutoff",
    },
}

calculate_points = None
data = main(name, scrap_urls, ignore_list, distance_from,scrape_file, archive_data_file, print_columns ,calculate_points = calculate_points, scoring_map = scoring_map )
#data = analyze_data(name, ignore_list, distance_from, scrape_file, archive_data_file, print_columns, calculate_points = calculate_points, scoring_map = scoring_map)

print(data.loc[(data.price > 0) & (data.points > 0)].sort_values(by="price", ascending = True)[["points", "price", "size", "url"]].to_string())


#message = "#####NEW: \n" +data["new"] +  "\n######TOP 20:\n" + data["top20"]
#send_mail(gmail_user, gmail_password,to, message)
