

class Landscape:
    def __init__(self, island):
        self.island = island
        self.fodder = 0
        self.animal = []


    def map_list(self):
        """string made to nested list"""
        self.list_island = [[i for i in j] for j in self.island.split()]
        return self.list_island

    def assign_tile(self):
        self.kart = []
        for i, e in enumerate(self.list_island):
            for j, n in enumerate(e):
                if n is 'O':
                    self.kart.append(Ocean(i+1, j+1))
                elif n is 'J':
                    self.kart.append(Jungle(i+1, j+1))
        return self.kart

    def fodder_added(self):
        pass

    def fodder_decreased(self):
        pass

    def animals(self):
        pass


class Jungle(Landscape):
    def __init__(self, x, y):
        self.fodder = 800
        self.coordinates = (x, y)


class Ocean(Landscape):
    def __init__(self, x, y):
        self.fodder = 0
        self.coordinates = (x, y)





