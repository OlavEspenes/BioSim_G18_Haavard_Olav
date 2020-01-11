

class Cell:

    def __init__(self, herbi, carni, fodder, h_parameters, c_parameters):
        self.herbi = []            # Liste med herbivores i gitt rute sortert etter fitness.
        self.carni = []            # Liste med carnivores i gitt rute sortert etter fitness.
        " Hvordan skal skal fitness kobles til riktig herbi/carni?

        self.fodder = None         # Hvor mye Fodder som er tilgjengelig i gitt rute.
        self.h_parameters = {}     # Parameters for herbivores.
        self.c_parameters = {}     # Parameters for carnivores.
        self.h_weight = []         # Tom liste som fylles med weight for herbivores.
        self.c_weight = []         # Tom liste som fylles med weight for carnivores.

        self.update_fitness()
        "Hvor skal update fitness plasseres?"

    def feeding_herbi(self):
        """Eats plants and removes fodder from cell.
        Eats by fitness order and gains weight.
        """
        for animal in self.herbi:
            appetite = self.h_parameters['F']
            if appetite <= self.fodder:
                self.weight = self.weight + h_parameters['beta'] * appetite
                landscape_location.food() =
            elif 0 < current_food < appetite:
                self.weight = self.weight + parameters['beta'] * current_food

    def feeding_carni(self):
        """Kills with a probability p.
        Removes herbovore and gains weight.
        Fitness is revaluated
        """
        pass


    def procreation(self):
        """Animals procreate by a probability.
        """
        pass



class Jungle(Cell):
    def __init__(self):

    def f_jungle(self):
        """Fodder eaten or grown???
        Available fodder?
        """

        pass

class Ocean(Cell):
    def __init__(self):



