# -*- coding: utf-8 -*-

"""

"""

__author__ = "Olav Vikøren Espenes & Håvard Brobakken Eig"
__email__ = "olaves@nmbu.no, havardei@nmbu.no"

import random
import math
import numpy as np


class Cell:

    def __init__(self, herbi, carni, fodder, herbi_para, carni_para):
        self.herbi = herbi
        self.carni = carni
        self.fodder = fodder
        self.h_parameters = herbi_para
        self.c_parameters = carni_para

    def fitness_single_animal(self, age, weight, parameters):
        q_plus = (1 + math.e ** (parameters['phi_age']
                                 * (age - parameters['a_half'])))
        q_minus = (1 + math.e ** (-parameters['phi_weight']
                                  * (weight - parameters['w_half'])))
        fitness = (q_plus * q_minus) ** -1
        return fitness

    def update_fitness_sorted(self, input_list, parameters):
        for i, j in enumerate(input_list):
            j['fitness'] = self.fitness_single_animal(
                input_list[i]['age'], input_list[i]['weight'], parameters)
        input_list.sort(key=lambda item: item.get('fitness'), reverse=True)

    def feeding_herbi(self):
        """
        All herbivores eat fodder and the remaining amount is returned.
        If all fodder is eaten, remaining herbivores won't eat.
        Eats in order of fitness and gains weight.
        """
        self.update_fitness_sorted(self.herbi, self.h_parameters)
        for animal, _ in enumerate(self.herbi):
            appetite = self.h_parameters['F']
            if appetite <= self.fodder:
                self.herbi[animal]['weight'] = self.herbi[animal]['weight'] \
                                               + self.h_parameters['beta'] \
                                               * appetite
                self.fodder = self.fodder - appetite

            elif 0 < self.fodder < appetite:
                self.herbi[animal]['weight'] = self.herbi[animal]['weight']\
                                               + self.h_parameters['beta'] \
                                               * self.fodder
                self.fodder = 0
            else:
                pass
        self.update_fitness_sorted(self.herbi, self.h_parameters)
        return self.fodder

    def feeding_carni(self):
        """
        Each carnivore evaluates each herbivore in order of their fitness.
        Herbivore with lowest fitness is evaluated first and has the
        highest probability to be eaten.
        Herbivore is removed from herbi list if eaten and the carnivore
        adds weight.
        """
        self.update_fitness_sorted(self.herbi, self.h_parameters)
        self.update_fitness_sorted(self.carni, self.c_parameters)
        herbi = sorted(self.herbi, key=lambda i: i['fitness'])

        for hunter, _ in enumerate(self.carni):
            dead_herbis = []
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

                            probability = random.random() < \
                                          ((self.carni[hunter]['fitness'] -
                                            herbi[preyer]['fitness']) /
                                           self.c_parameters['DeltaPhiMax'])
                            if probability is True:
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

                    elif 0 < appetite < herbi[preyer]['weight']:
                        if self.carni[hunter]['fitness'] <= \
                                herbi[preyer]['fitness']:
                            continue

                        elif 0 < self.carni[hunter]['fitness'] - \
                                herbi[preyer]['fitness'] < \
                                self.c_parameters['DeltaPhiMax']:
                            probability = random.random() < \
                                          ((self.carni[hunter]['fitness']
                                               - herbi[preyer]['fitness'])
                                              / self.c_parameters['DeltaPhiMax'])

                            if probability is True:
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

            for animal, _ in enumerate(dead_herbis):
                if dead_herbis[animal] in self.herbi:
                    self.herbi.remove(dead_herbis[animal])

    def procreation(self, list_animal, parameters, species):
        """
        Adds animal to input list by probability based on fitness and
        'gamma' parameter. Probability becomes zero if the mothers
        weight is the offsprings weight times 'zeta'.
        Newborns weight is set to 0.
        """
        self.update_fitness_sorted(list_animal, parameters)
        newborns = []
        for i, _ in enumerate(list_animal):
            weight = parameters['w_birth'] + np.random.normal() * \
                     parameters['sigma_birth']
            p = parameters['gamma'] * list_animal[i].get('fitness') \
                * (len(list_animal) - 1)
            if p > random.random() and list_animal[i].get('weight') \
                    > parameters['zeta'] * weight:
                check_mother_weight = list_animal[i].get('weight') - weight * \
                                      parameters['xi']
                if check_mother_weight > 0:
                    newborns.append(
                        {'species': species, 'age': 0, 'weight': weight})
                    list_animal[i]['weight'] = list_animal[i].get('weight') \
                                               - weight * parameters['xi']
        for add in newborns:
            list_animal.append(add)

    def birth(self):
        """
        Uses procreation function to modify herbi and carni list.
        """
        self.update_fitness_sorted(self.herbi, self.h_parameters)
        self.update_fitness_sorted(self.carni, self.c_parameters)
        self.procreation(self.herbi, self.h_parameters, 'Herbivore')
        self.procreation(self.carni, self.c_parameters, 'Carnivore')

    def age(self):
        """
        Adds 1 to age in herbi and carni list.
        """
        for i, _ in enumerate(self.carni):
            self.carni[i]['age'] += 1
        for i, _ in enumerate(self.herbi):
            self.herbi[i]['age'] += 1

    def weight_loss(self):
        """
        Reduces weight by parameter 'eta' in herbi and carni list.
        """
        for i, _ in enumerate(self.carni):
            self.carni[i]['weight'] -= \
                self.carni[i]['weight'] * self.c_parameters['eta']
        for i, _ in enumerate(self.herbi):
            self.herbi[i]['weight'] -= \
                self.herbi[i]['weight'] * self.h_parameters['eta']

    def death_function(self, list_animal, parameters):
        """
        Modifies a list with animal. Goes through list and removes each animal
        with a certain probability based on fitness and parameter 'omega'.
        """
        self.update_fitness_sorted(list_animal, parameters)
        should_del = []
        for a, _ in enumerate(list_animal):
            if list_animal[a].get('fitness') < 0 or \
                    list_animal[a].get('weight') <= 0:
                should_del.append(list_animal[a])
        for el in should_del:
            list_animal.remove(el)

        should_del2 = []
        for b, _ in enumerate(list_animal):
            p_death = parameters['omega'] * (1 - list_animal[b].get('fitness'))
            if p_death > random.random():
                should_del2.append(list_animal[b])
        for el in should_del2:
            list_animal.remove(el)


    def death(self):
        """uses simple death function and updates herbi and carni
        with fewer animals after natural death"""
        self.update_fitness_sorted(self.herbi, self.h_parameters)
        self.update_fitness_sorted(self.carni, self.c_parameters)
        self.death_function(self.carni, self.c_parameters)
        self.death_function(self.herbi, self.h_parameters)

    def who_will_migrate(self, list_animal, parameter):
        """Make migration list as output from this function
        and remove from list her in cell
        """
        self.update_fitness_sorted(list_animal, parameter)
        migrant = []
        emigrant = []
        for animal, _ in enumerate(list_animal):
            p = parameter['mu'] * list_animal[animal].get('fitness')
            if p > random.random():
                migrant.append(list_animal[animal])
                emigrant.append(list_animal[animal])
        for el in migrant:
            list_animal.remove(el)
        return emigrant

    def send_out_emigrators(self):
        herbi_migration_list = self.who_will_migrate(self.herbi,
                                                     self.h_parameters)
        carni_migration_list = self.who_will_migrate(self.carni,
                                                     self.c_parameters)
        return herbi_migration_list, carni_migration_list
