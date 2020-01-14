# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

import random
import math
import numpy as np
from animal import Animal


class Cell:

    def __init__(self, herbi, carni, fodder, herbi_para, carni_para, position):


        self.herbi = sorted(herbi, key=itemgetter('fitness'), reverse = True)
            # Liste med herbivores med dictionary med egenskapene age, weight og fitness
            # i gitt rute sortert etter fitness.

        self.carni = sorted(carni, key=itemgetter('fitness'), reverse = True)
            # Samme liste med dictionary for cornivores.
        self.position = position
        """
        "Eksempel:
    
        self.herbi = [{'age': 10, 'fitness': 30, 'weight': 15},
                        {'age': 5, 'fitness': 25, 'weight': 40},
                        {'age': 15, 'fitness': 20, 'weight': 25}]
        self.carni = [{'age': 3, 'fitness': 40, 'weight': 35},
                        {'age': 5, 'fitness': 35, 'weight': 20},
                        {'age': 8, 'fitness': 30, 'weight': 5}]
        """

        self.fodder = fodder         # Hvor mye Fodder som er tilgjengelig i gitt rute.
        self.h_parameters = herbi_para     # Parameters for herbivores.
        self.c_parameters = carni_para     # Parameters for carnivores.
        self.animal = Animal(herbi_para, cardi_para)

    def feeding_herbi(self):
        """Eats plants and removes fodder from cell.
        Eats by fitness order and gains weight.
        """
        for animal,_ in enumerate(self.herbi):
            appetite = self.h_parameters['F']
            if appetite <= self.fodder:
                self.herbi[animal]['weight'] = self.herbi[animal]['weight']\
                                               + self.h_parameters['beta'] * appetite
                self.herbi[animal]['fitness'] = self.animal.update_fitness_herbi\
                    (self.herbi[animal]['age'], self.herbi[animal]['weight'])
                self.fodder = self.fodder - appetite

            elif 0 < self.fodder < appetite:
                self.herbi[animal]['weight'] = self.herbi[animal]['weight']\
                                               + self.h_parameters['beta'] * self.fodder
                self.herbi[animal]['fitness'] = self.animal.update_fitness_herbi\
                    (self.herbi[animal]['age'], self.herbi[animal]['weight'])
                self.fodder = 0
            else:
                pass
                # function that reduces food in cell
                # update fitness



    def feeding_carni(self):
        """Kills with a probability p.
        Removes herbovore and gains weight.
        Fitness is revaluated
        """
        


    def procreation_herbi(self):#kanskje? input liste? eller enkeltdyr?
        """Animals procreate by a certain probability.
        probability 0: w < c(w-birth + o-birth)
        Mother loose weight. Too much and no kiddie.
        """
        for animal, _ in enumerate(self.herbi):
            weight = self.h_parameters['w_birth'] + np.random.normal() * \
                     self.h_parameters['sigma_birth']
            p = self.h_parameters['gamma'] * self.herbi[animal].get('fitness')\
                * (len(self.herbi) - 1)
            if p > random.random(): #and self.h_parameters['omega']\
                    #> self.h_parameters['zeta'] * weight:
                #add animal with age 0 and weight
                check_mother_weight = self.herbi[i].get('weight') - weight * \
                                      self.h_parameters['xi']
                if check_mother_weight > 0:
                    self.herbi.append({'species': 'Herbivore', 'age': 0,
                                  'weight': weight})
                    self.herbi[i]['weight'] = self.herbi[i].get('weight') - weight * \
                                         self.h_parameters['xi']
            #else:
                #no animal and nothing happens

    def age(self):
        """Updates all ages by 1 year in
        carni and herni lists.
        Fitness should maybe also be updated???????????????????????????
        """
        for i, _ in enumerate(self.carni):
            self.carni[i]['age'] += 1
        for i, _ in enumerate(self.herbi):
            self.herbi[i]['age'] += 1

    def weight_loss(self):
        for i, _ in enumerate(self.carni):
            self.carni[i]['weight'] -= \
                self.carni[i]['weight'] * self.c_parameters['eta']
        for i, _ in enumerate(self.herbi):
            self.herbi[i]['weight'] -= \
                self.herbi[i]['weight'] * self.h_parameters['eta']

    def simple_death(self, list_animal, parameters):
        should_del = []
        for a, _ in enumerate(list_animal):
            if list_animal[a].get('fitness') < 0:
                should_del.append(list_animal[a])
        for el in should_del:
            list_animal.remove(el)

        should_del2 = []
        for b, _ in enumerate(list_animal):
            p_death = parameters['omega'] * (
                        1 - list_animal[b].get('fitness'))
            if p_death > random.random():
                should_del2.append(list_animal[b])
        for el in should_del2:
            list_animal.remove(el)

    def natural_death(self): #NB!! make sure fitness is updated before use
        """uses simple death function and updates herbi and carni
        with fewer animals after natural death"""
        self.simple_death(self.carni, self.c_parameters)
        self.simple_death(self.herbi, self.h_parameters)


    def who_will_migrate(self, list_animal, parameter):
        """Make migration list as output from this function
        and remove from list her in cell
        """
        migrating_herbi = []
        for animal, _ in enumerate(list_animal):
            p = parameter('mu') * list_animal[animal].get('fitness')
            if p > random.random():
                migrating_herbi.append(list_animal[animal])
        for el in migrating_herbi:
            list_animal.remove(el)
        return migrating_herbi

    def where_to_migrate(self):
        herbi_migration_list = self.who_will_migrate(self.herbi, self.h_parameters)
        carni_migration_list = self.who_will_migrate(self.carni, self.c_parameters)
        


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



