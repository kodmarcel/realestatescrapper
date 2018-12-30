import json
from apartment import Apartment

class ApartmentsEncoder(json.JSONEncoder):
    def default(self,z):
        if isinstance(z, Apartment):
            return z.__dict__
        else:
            super().default(self, z)


class ApartmentsDecoder(json.JSONDecoder):
    def object_hook(object):
        try:
            if "link" in object and "price" in object:
                return Apartment(object["link"],object["price"],object["size"],object["location"],object["floor"],object["built"],object["renewed"],object["distance"])
        except Exception as e:
            print(e)
            print("Couldnt desetialize: ")
            print(object)
