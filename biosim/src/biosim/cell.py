
import random


class Cell:

    def __init__(self, herbi, carni, fodder, herbi_parameters, carni_parameters):


        self.herbi = sorted(herbi, key=itemgetter('fitness'), reverse = True)
            # Liste med herbivores med dictionary med egenskapene age, weight og fitness
            # i gitt rute sortert etter fitness.

        self.carni = sorted(carni, key=itemgetter('fitness'), reverse = True)
            # Samme liste med dictionary for cornivores.
        """
        "Eksempel:
    
        self.herbi = [{'age': 10, 'fitness': 30, 'weight': 15},
                        {'age': 5, 'fitness': 25, 'weight': 40},
                        {'age': 15, 'fitness': 20, 'weight': 25}]
        self.carni = [{'age': 3, 'fitness': 40, 'weight': 35},
                        {'age': 5, 'fitness': 35, 'weight': 20},
                        {'age': 8, 'fitness': 30, 'weight': 5}]
        """

        self.fodder = None         # Hvor mye Fodder som er tilgjengelig i gitt rute.
        self.h_parameters = {}     # Parameters for herbivores.
        self.c_parameters = {}     # Parameters for carnivores.

        self.update_fitness()
        "Hvor skal update fitness plasseres?"

    def feeding_herbi(self):
        """Eats plants and removes fodder from cell.
        Eats by fitness order and gains weight.
        """
        for animal in self.herbi:
            appetite = self.h_parameters['F']
            if appetite <= self.fodder:
                self.herbi[] = self.weight + h_parameters['beta'] * appetite
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



