#!/bin/bash

PROJECT_FOLDER="/home/marcel/Projects/RealEstateScrapper/"

TO="salmic.marcel@gmail.com"
FROM="real-estate-checker@desktop.com"

cd $PROJECT_FOLDER

CURRENT_ADDS=$(python estates.py)

logger -t realestatechecker -- Checked for new real estate adds

echo "Subject: Newest real estate adds
Today's newest real estates:
$CURRENT_ADDS" | sendmail -f ${FROM} ${TO}
