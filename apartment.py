class Apartment:

    def __init__(self, link, price, size, location, floor, built, renewed, distance):
        self.link = link
        self.price = price if isinstance(price,float) else float(price)
        self.size = size if isinstance(size,float) else float(size)
        self.location = location
        try:
            self.floor = floor if isinstance(floor,int) else int(floor.split("/")[0])
        except:
            self.floor = -1
        self.built = built if isinstance(built,int) else int(built)
        self.renewed = renewed if isinstance(renewed,int) else int(renewed)
        self.distance = distance
        self.points = 0


    def calculate_points(self):
        try:
            price_points = -self.price/1000 * 2.5
            size_points = self.size * 2.5
            per_meter = - (self.price/1000 / self.size) * 2
            build_points = (self.built-1940)/2 if self.built != -1 else 0
            renewed_points = (self.renewed-1990)/4 if self.renewed != -1 else 0
            if self.floor == 0:
                floor_points = -25
            elif self.floor == -1:
                floor_points = 0
            elif self.floor  < 5:
                floor_points = 10
            elif self.floor  < 11:
                floor_points = -10
            else:
                floor_points = 10

            if self.distance == -1:
                distance_points = -30
            elif self.distance < 2:
                distance_points = 40
            elif self.distance < 4:
                distance_points = 20
            elif self.distance < 6:
                distance_points = 5
            else:
                distance_points = -self.distance*100
            self.points = price_points + per_meter + size_points + build_points + renewed_points+ floor_points + distance_points
        except Exception as e:
            print(e)
            print("Couldn't calculate points for : ")
            print(self)


    def __str__(self):
        return "Stanovanje: " + "\n" + \
        "Točke: " + str(self.points) + ", " + "\n" + \
        "Cena: " + str(self.price) + ", " + "\n" + \
        "Velikost: " + str(self.size) + ", " + "\n"+ \
        "€/m2: " + str(self.price/self.size) + ", " + "\n" + \
        "Nadstropje: " + str(self.floor) + ", " + "\n" + \
        "Razdalja: " + str(self.distance) + ", " + \
        "Lokacija: " + str(self.location) + ", " + "\n" + \
        "Link: " + str(self.link) + ", " + "\n" + \
        "Zgrajeno: " + str(self.built) + ", " + \
        "Obnovnljeno: " + str(self.renewed) + ", "
