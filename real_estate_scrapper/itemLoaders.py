from scrapy.loader import ItemLoader
from scraly.loader.processors import MapCompose, Join

def parseInt(self, values):
    for value in values:
        yield int(value)

class NepremicnineEstateLoader(ItemLoader):
    size_in = parseSize
    built_in = parseInt
    renewed_in = parseInt
    price_in = parsePrice 

    def parseSize(self, values):
        for value in values:
            number = value.split(" ")[0].strip().replace(",", ".").replace('"', '')
            yield float(number)
    
    def parsePrice(self, values):
        for value in values:
            number = value.split(" ")[0].strip().replace(".", "").replace(",",".").replace('"','')
            yield float(number)
    
