
import random
class Cell:

    def __init__(self, herbi, carni, fodder, herbi_parameters, carni_parameters):
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
                #function that reduces food in cell
                #update fitness
                landscape_location.food() =
            elif 0 < current_food < appetite:
                self.weight = self.weight + parameters['beta'] * current_food
                # function that reduces food in cell
                # update fitness



    def feeding_carni(self):
        """Kills with a probability p.
        Removes herbovore and gains weight.
        Fitness is revaluated
        """
        pass


    def procreation(self):#kanskje? input liste? eller enkeltdyr?
        """Animals procreate by a certain probability.
        probability 0: w < c(w-birth + o-birth)
        Mother loose weight. Too much and no kiddie.
        """
        for animal in self.herbi:
            weight = self.h_parameters['w_birth'] + np.random.normal() * \
                     self.h_parameters['sigma_birth']
            p = self.h_parameters('gamma') * self.herbi[animal].get('fitness')\
                * (len(self.herbi) - 1)
            if p > random.random() and self.h_parameters['omega']\
                    > self.h_parameters['zeta'] * weight:
                #add animal with age 0 and weight
                self.herbi.append({'species':'Carnivore', 'age':0,
                                   'weight':weight})
            else:
                #no animal and nothing happens

class Jungle(Cell):
    def __init__(self):

    def f_jungle(self):
        """Fodder eaten or grown???
        Available fodder?
        """
        pass

class Savanna(Cell):
    def __init__(self):

    def f_savanna(self):
        """Fodder eaten or grown???
        Available fodder?
        """
        pass

class Ocean(Cell):
    def __init__(self):



