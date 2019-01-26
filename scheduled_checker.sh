#!/bin/bash

PROJECT_FOLDER="/home/marcel/Projects/RealEstateScrapper/"

ARCHIVE_REPORTS="reports/report_"
NOW=$(date +'%Y_%m_%d') 


#TO="salmic.marcel@gmail.com, aneja.kutin@gmail.com, st-3-3tg7u3u59v@glockapps.com"
TO="salmic.marcel@gmail.com, aneja.kutin@gmail.com"
FROM="real-estate-checker@desktop.com"


cd $PROJECT_FOLDER

find $PROJECT_FOLDER$ARCHIVE_REPORTS* -mtime +7 -exec rm{} \;


echo "Scraping estates data"
logger -t realestatechecker -- Scraping estates data 

cp scraped_data/nepremicnine.csv scraped_data/nepremicnine.csv.old
cp scraped_data/bolha.csv scraped_data/bolha.csv.old
cp scraped_data/mojikvadrati.csv scraped_data/mojikvadrati.csv.old

cp analyzed_data/estates.csv analyzed_data/estates.csv.old

scrapy crawl nepremicnine -o scraped_data/nepremicnine.csv
scrapy crawl bolha -o scraped_data/bolha.csv
scrapy crawl mojikvadrati -o scraped_data/mojikvadrati.csv


echo " Analyzing estates data"
logger -t realestatechecker -- Analyzing estates data 

CURRENT_ADDS=$(python real_estate_analysis/estate_analysis.py)

logger -t realestatechecker -- Checked for new real estate adds

echo "Newest real estate adds 
Today's newest real estates - $NOW:
$CURRENT_ADDS" > $PROJECT_FOLDER$ARCHIVE_REPORTS$NOW


echo "Subject: Newest real estate adds
Today's newest real estates - $NOW:
$CURRENT_ADDS" | sendmail -f ${FROM} ${TO}

