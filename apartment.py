class Apartment:

    def __init__(self, link, price, size, location, floor, built, renewed):
        self.link = link
        self.price = price
        self.size = size
        self.location = location
        self.floor = floor
        self.built = built
        self.renewed = renewed
    
    def __str__(self):
        return "Apartment: \n  " +  str(self.__dict__) 
