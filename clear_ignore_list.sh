# Checks if links on ignore list are obsolete as they no longer exist

ignore_file=/home/marcel/Projects/RealEstateScrapper/ignored_estates
temp_file=/home/marcel/Projects/RealEstateScrapper/ignored_estates.temp

while read url; do

add=$(wget -qO- $url)
if [ -z "$add" ] || [ "$add" == *"ni več aktivna"* ] ; then
	echo "Deleting url: " $url
	continue
fi
echo $url >> temp_file 
done <$ignore_file

mv $temp_file $ignore_file
