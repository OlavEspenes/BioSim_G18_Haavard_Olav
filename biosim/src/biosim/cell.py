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
        self.herbi = herbi
            # Liste med herbivores med dictionary med egenskapene age, weight og fitness
            # i gitt rute sortert etter fitness.

        self.carni = carni
            # Samme liste med dictionary for cornivores.
        self.position = position
        """
        "Eksempel:
    
        self.herbi = [{'age': 10, 'species: 'Herbivore', 'weight': 15},
                        {'age': 5, 'species: 'Herbivore', 'weight': 40},
                        {'age': 15, 'species: 'Herbivore', 'weight': 25}]
        self.carni = [{'age': 3, 'species: 'Carnivore', 'weight': 35},
                        {'age': 5, 'species: 'Carnivore', 'weight': 20},
                        {'age': 8, 'species: 'Carnivore', 'weight': 5}]
        """

        self.fodder = fodder         # Hvor mye Fodder som er tilgjengelig i gitt rute.
        self.h_parameters = herbi_para     # Parameters for herbivores.
        self.c_parameters = carni_para     # Parameters for carnivores.

    def fitness_single_animal(self, age, weight, parameters):
        q_plus = (1 + math.e ** (parameters['phi_age']
                                 * (age - parameters['a_half'])))
        q_minus = (1 + math.e ** (-parameters['phi_weight']
                                  * (weight - parameters['w_half'])))
        fitness = (q_plus * q_minus) ** -1
        return fitness

    def update_fitness_sorted(self, input_list, parameters):
        for i in input_list:
            i['fitness'] = fitness_singel_animal(input_list[i]['age'],
                                  input_list[i]['weight'], parameters)
        sorted(input_list, key=lambda j: j['fitness'], reverse=True)


    def feeding_herbi(self):
        """Eats plants and removes fodder from cell.
        Eats by fitness order and gains weight.
        """
        self.update_fitness_sorted(self.herbi, self.h_parameters)
        for animal,_ in enumerate(self.herbi):
            appetite = self.h_parameters['F']
            if appetite <= self.fodder:
                self.herbi[animal]['weight'] = self.herbi[animal]['weight']\
                                               + self.h_parameters['beta'] * appetite
                self.fodder = self.fodder - appetite

            elif 0 < self.fodder < appetite:
                self.herbi[animal]['weight'] = self.herbi[animal]['weight']\
                                               + self.h_parameters['beta'] * self.fodder
                self.fodder = 0
            else:
                pass
        self.update_fitness_sorted(self.herbi, self.h_parameters)
                # function that reduces food in cell


    def feeding_carni(self):
        """Kills with a probability p.
        Removes herbovore and gains weight.
        Fitness is revaluated
        """
        dead_herbis = []
        herbi = sorted(self.herbi, key=lambda i: i['fitness'])

        for hunter, _ in enumerate(self.carni):
            appetite = self.c_parameters['F']
            for preyer, _ in enumerate(herbi):
                if appetite > 0:
                    if herbi[preyer]['weight'] <= appetite:
                        if self.carni[hunter]['fitness'] <= \
                                herbi[preyer]['fitness']:
                            continue
                        elif 0 < self.carni[hunter]['fitness'] - \
                                herbi[preyer]['fitness'] < \
                                self.c_parameters['DeltaPhiMax']:

                            propability = random.random() < \
                                          ((self.carni[hunter]['fitness'] -
                                            herbi[preyer]['fitness']) /
                                           self.c_parameters['DeltaPhiMax'])
                            if propability is True:
                                self.carni[hunter]['weight'] = \
                                    self.carni[hunter]['weight'] + \
                                    self.c_parameters['beta'] * \
                                    herbi[preyer]['weight']

                                self.carni[hunter]['fitness'] = \
                                    self.fitness_single_animal(
                                    self.carni[hunter]['age'],
                                    self.carni[hunter]['weight'],
                                        self.c_parameters)
                                dead_herbis.append(herbi[preyer])
                                appetite = appetite - herbi[preyer]['weight']
                            else:
                                continue
                        else:
                            self.carni[hunter]['weight'] = \
                                self.carni[hunter]['weight'] + \
                                self.c_parameters['beta'] * \
                                herbi[preyer]['weight']

                            self.carni[hunter]['fitness'] = \
                                self.fitness_single_animal(
                                    self.carni[hunter]['age'],
                                    self.carni[hunter]['weight'],
                                    self.c_parameters)
                            dead_herbis.append(herbi[preyer])
                            appetite = appetite - herbi[preyer]['weight']

                    elif 0 < appetite < herbi['preyer']['weight']:

                        if self.carni[hunter]['fitness'] <= \
                                herbi[preyer]['fitness']:
                            continue

                        elif 0 < self.carni[hunter]['fitness'] - \
                                herbi[preyer]['fitness'] < \
                                self.carni_para['DeltaPhiMax']:
                            propability = random.random() < \
                                          ((self.carni[hunter]['fitness']
                                               - herbi[preyer]['fitness'])
                                              / self.carni_para['DeltaPhiMax'])

                            if propability is True:
                                self.carni[hunter]['weight'] = \
                                    self.carni[hunter]['weight'] + \
                                    self.c_parameters['beta'] * appetite
                                self.carni[hunter]['fitness'] = \
                                    self.fitness_single_animal\
                                        (self.carni[hunter]['age'],
                                         self.carni[hunter]['weight'],
                                         self.c_parameters)
                                dead_herbis.append(herbi[preyer])
                                appetite = appetite - appetite
                                if appetite != 0:
                                    raise ValueError("Wrong in appetite list")
                                else:
                                    break
                            else:
                                continue
                        else:
                            self.carni[hunter]['weight'] = \
                                self.carni[hunter]['weight'] + \
                                self.c_parameters['beta'] * appetite
                            self.carni[hunter]['fitness'] = \
                                self.fitness_single_animal(
                                self.carni[hunter]['age'],
                                self.carni[hunter]['weight'],
                                    self.c_parameters)

                            dead_herbis.append(herbi[preyer])
                            appetite = appetite - appetite

                            if appetite != 0:
                                raise ValueError("Wrong in appetite list")
                            else:
                                break
                    else:
                        break
                else:
                    break

    def procreation(self, list_animal, parameters):#kanskje? input liste? eller enkeltdyr?


    def procreation(self, list_animal, parameters, species):
        """Animals procreate by a certain probability.
        probability 0: w < c(w-birth + o-birth)
        Mother loose weight. Too much and no kiddie.
        """
        newborns = []
        for i, _ in enumerate(list_animal):
            weight = parameters['w_birth'] + np.random.normal() * \
                     parameters['sigma_birth']
            p = parameters['gamma'] * list_animal[i].get('fitness') * (len(list_animal) - 1)
            if p > random.random(): #and self.h_parameters['omega']\
                    #> self.h_parameters['zeta'] * weight:
                #add animal with age 0 and weight
                check_mother_weight = list_animal[i].get('weight') - weight * \
                                      parameters['xi']
                if check_mother_weight > 0:
                    newborns.append({'species': species, 'age': 0,
                                  'weight': weight})
                    list_animal[i]['weight'] = list_animal[i].get('weight') - \
                                               weight * parameters['xi']
        for add in newborns:
            list_animal.append(add)

    def birth(self):
        self.update_fitness_sorted(self.herbi, self.h_parameters)
        self.update_fitness_sorted(self.carni, self.c_parameters)
        self.procreation(self.herbi, self.h_parameters,'herbivore')
        self.procreation(self.carni, self.c_parameters,'carnivore')

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

    def death_function(self, list_animal, parameters):
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

    def death(self): #NB!! make sure fitness is updated before use
        """uses simple death function and updates herbi and carni
        with fewer animals after natural death"""
        self.death_function(self.carni, self.c_parameters)
        self.death_function(self.herbi, self.h_parameters)

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
        


"""
if __name__ == "__main__":
    print(Cell())



class Jungle(Cell):
    def __init__(self):

    def f_jungle(self):
        #Fodder eaten or grown???
        #Available fodder?
        
        pass

class Savanna(Cell):
    def __init__(self):

    def f_savanna(self):
        
        pass

class Ocean(Cell):
    def __init__(self):

"""






