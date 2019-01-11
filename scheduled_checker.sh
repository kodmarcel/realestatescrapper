#!/bin/bash

PROJECT_FOLDER="/home/marcel/Projects/RealEstateScrapper/"

#TO="salmic.marcel@gmail.com, aneja.kutin@gmail.com, st-3-3tg7u3u59v@glockapps.com"
TO="salmic.marcel@gmail.com, aneja.kutin@gmail.com"
FROM="real-estate-checker@desktop.com"


cd $PROJECT_FOLDER



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

echo "Subject: Newest real estate adds
Today's newest real estates:
$CURRENT_ADDS" | sendmail -f ${FROM} ${TO}

