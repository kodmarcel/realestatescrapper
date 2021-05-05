from run import main, analyze_data

run_name = "example_buy_to_rent"
scrap_urls = ["https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/cena-do-180000-eur/?nadst%5B0%5D=vsa&nadst%5B1%5D=vsa", "https://www.bolha.com/prodaja-stanovanja?geo%5BlocationIds%5D=44267%2C44265%2C44269%2C44270%2C26590&price%5Bmax%5D=180000&typeOfTransaction=sell"]
distance_from = "Jamova cesta 39, Ljubljana, Slovenija"
ignore_list = []
archive_data_file = "archive_data/" + run_name + ".csv"
print_columns = ["points", "location", "price", "size", "distance", "captured_today", "url"]


scoring_map = {
    "price": [{
        "type": "reverse",
        "points_per_unit": 1
    },
    {
        "type": "lower_than",
        "value": 1500,
        "points": -5000000000
    },
    {
        "type": "lower_than",
        "value": 8500,
        "points": -500000
    },
    {
        "type": "greater_than",
        "value": 160000,
        "points": -1000000
    }],
    "built": {
        "type": "normal",
        "points_per_unit": 500
    },
    "size": {
        "type": "normal",
        "points_per_unit": 2000,
    },
    "distance": {
        "type": "reverse",
        "points_per_unit": 4000,
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
#data = main(run_name, scrap_urls, ignore_list, distance_from,archive_data_file, print_columns ,calculate_points = calculate_points, scoring_map = scoring_map )
data = analyze_data(run_name, ignore_list, distance_from, archive_data_file, print_columns, calculate_points = calculate_points, scoring_map = scoring_map)

print(data.loc[(data.price > 0) & (data.points > 0)].sort_values(by="price", ascending = True)[["points", "price", "size", "url"]].to_string())


#message = "#####NEW: \n" +data["new"] +  "\n######TOP 20:\n" + data["top20"]
#send_mail(gmail_user, gmail_password,to, message)
