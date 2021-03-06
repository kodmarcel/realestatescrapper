from run import main,analyze_data, send_mail
import smtplib

gmail_user = "mail_for_sending@gmail.com"
gmail_password = "password"
to = ["mail1@gmail.com", "mail2@email.com"]

name = "example_rent"
scrap_urls = ["https://www.nepremicnine.net/oglasi-oddaja/ljubljana-mesto/stanovanje/garsonjera,1-sobno,1.5-sobno,2-sobno,2.5-sobno/cena-od-200-do-1200-eur-na-mesec/?nadst%5B0%5D=vsa&nadst%5B1%5D=vsa", "https://www.bolha.com/oddaja-stanovanja?geo%5BlocationIds%5D=44270%2C44269%2C44267%2C44265%2C44268%2C26590&price%5Bmin%5D=200&price%5Bmax%5D=1200&numberOfRooms%5Bmin%5D=studio-apartment&numberOfRooms%5Bmax%5D=twoHalf-room"]
distance_from = "Kongresni trg, Ljubljana, Slovenija"
ignore_list = ["oddamo sob","oddam sob","oddaja se sob", "oddajam sobo", "študentsko sobo", "oddaja se postelj","oddaja postelj","oddamo postelj", "oddamo dvoposteljno", "souporab","delit", "skupno", "že stanuje", "oddamo posteljo", "postelji oddamo", ]
scrape_file = "scraped_data/" + name + ".csv"
archive_data_file = "archive_data/" + name + ".csv"
print_columns = ["points", "location", "price", "size", "distance", "captured_today", "url"]


scoring_map = {
            "price": {
            "type": "reverse",
             "points_per_unit": 1
            },
            "built": {
            "type": "normal",
            "points_per_unit": 10
             },
            "size": {
            "type": "normal",
            "points_per_unit": 10,
            },
            "distance": {
            "type": "reverse",
            "points_per_unit": 50,
            },
            "floor": {
            "type": "contains",
            "values": ["PK"],
            "points": -100
            },
             "active": {
            "type": "cutoff",
            },
}

calculate_points = None
data = main(name, scrap_urls, ignore_list, distance_from, archive_data_file, print_columns ,calculate_points = calculate_points, scoring_map = scoring_map )
#data = analyze_data(name, ignore_list, distance_from, archive_data_file, print_columns, calculate_points = calculate_points, scoring_map = scoring_map)


message = "#####NEW: \n" +data["new"] +  "\n######TOP 20:\n" + data["top20"]
send_mail(gmail_user, gmail_password,to, message)
