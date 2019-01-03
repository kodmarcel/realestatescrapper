#!/bin/bash

PROJECT_FOLDER="/home/marcel/Projects/RealEstateScrapper/"

TO="salmic.marcel@gmail.com"
TO_2="aneja.kutin@gmail.com"
FROM="real-estate-checker@desktop.com"


cd $PROJECT_FOLDER



echo "Scraping estates data"
logger -t realestatechecker -- Scraping estates data 

rm scraped_data/nepremicnine.csv
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

echo "Subject: Newest real estate adds
Today's newest real estates:
$CURRENT_ADDS" | sendmail -f ${FROM} ${TO_2}

