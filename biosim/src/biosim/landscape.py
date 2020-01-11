
import copy
import numpy as np


class Landscape:
    def __init__(self, island):
        self.island = island
        self.fodder = 0
        self.animal = []
        self.cells = None
        self.herbivores_on_island = None

    def string_to_matrix(self):
        """string made to nested list"""
        temp = copy.deepcopy(self.island.replace(" ", ""))
        list_map = [[i for i in j] for j in temp.split()]
        return list_map

    """
    def array_cont(self):
        listed_map = self.string_to_matrix()
        array_shape = np.shape(listed_map)

        nested = list(np.zeros(array_shape))
        for i, e in enumerate(nested):
            nested[i] = list(e)

        self.cells = np.array(nested)
    """

    def assign_tile(self):
        self.kart = []
        for i, e in enumerate(self.string_to_matrix()):
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





