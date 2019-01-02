from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst

def parseInt(self, values):
    for value in values:
        yield int(value)

def parseSize(self, values):
    for value in values:
        number = value.split(" ")[0].strip().replace(",", ".").replace('"', '')
        yield float(number)
    
def parsePrice(self, values):
    for value in values:
        number = value.split(" ")[0].strip().replace(".", "").replace(",",".").replace('"','')
        yield float(number)
    
class NepremicnineEstateLoader(ItemLoader):
    default_output_processor = TakeFirst()
    size_in = parseSize
    built_in = parseInt
    renewed_in = parseInt
    price_in = parsePrice 

class MojikvadratiEstateLoader(ItemLoader):
    default_output_processor = TakeFirst()
    size_in = parseSize
    built_in = parseInt
    renewed_in = parseInt
    price_in = parsePrice 
