# -*- coding: utf-8 -*-

"""
"""

__author__ = "Olav Vikøren Espenes & Håvard Brobakken Eig"
__email__ = "olaves@nmbu.no, havardei@nmbu.no"

import random
import math
import numpy as np


class Cell:
    """
    A class with methods to be used for a annual cycle in one cell.
    """

    def __init__(self, herbi, carni, fodder, herbi_para, carni_para):

        """
        ==============   ==================================================
            *herbi*       A list with dictionaries, one for each herbivore.
            *carni*       A list with dictionaries, one for each carnivore.
            *fodder*      Amount of plant fodder available based on type.
         *herbi_para*           Dictionary of herbivore parameters.
         *carni_para*           Dictionary of carnivore parameters.
        ==============   ==============================================
        """

        self.herbi = herbi
        self.carni = carni
        self.fodder = fodder
        self.h_parameters = herbi_para
        self.c_parameters = carni_para

    def fitness_single_animal(self, age, weight, parameters):
        """
        Method to calculate fitness for a animal.

        :param age: Age of the animal.
        :param weight: Weight of the animal.
        :param parameters: Input parameters for
        :return: Returns fitness for one animal based on formulas (3) and (4)
                on page 3 in "Modelling the Ecosystem of Rossumøya".
        """
        q_plus = (1 + math.e ** (parameters['phi_age']
                                 * (age - parameters['a_half'])))
        q_minus = (1 + math.e ** (-parameters['phi_weight']
                                  * (weight - parameters['w_half'])))
        fitness = (q_plus * q_minus) ** -1
        return fitness

    def update_fitness_sorted(self, input_list, parameters):
        """
        Method to calculate fitness to all animals in a list.
        :param input_list: List with animals of same species.
        :param parameters: Corresponding parameters to specie in input_list.
        :return: Updated fitness for the animals in input list.
        """
        if input_list is not None:
            for i, j in enumerate(input_list):
                j['fitness'] = self.fitness_single_animal(
                    input_list[i]['age'], input_list[i]['weight'], parameters)
            input_list.sort(key=lambda item: item.get('fitness'), reverse=True)
        else:
            pass

    def feeding_herbi(self):
        """
        All herbivores eat fodder and the remaining amount is returned.
        If all fodder is eaten, remaining herbivores won't eat.
        Eats in order of fitness, from highest to lowest, and gains weight.
        """
        if self.fodder < 0:
            raise ValueError('Fodder cannot be negative')
        self.update_fitness_sorted(self.herbi, self.h_parameters)
        for animal, _ in enumerate(self.herbi):
            appetite = self.h_parameters['F']
            if appetite <= self.fodder:
                self.herbi[animal]['weight'] = self.herbi[animal]['weight'] \
                                               + self.h_parameters['beta'] \
                                               * appetite
                self.fodder -= appetite

            elif 0 < self.fodder < appetite:
                self.herbi[animal]['weight'] = self.herbi[animal]['weight'] \
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
        return self.herbi

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
                    list_animal[i]['weight'] = \
                        list_animal[i].get('weight') - weight \
                        * parameters['xi']
        for add in newborns:
            list_animal.append(add)

    def birth(self):
        """
        Uses procreation function to modify herbi and carni list.
        """
        herbi = self.herbi
        carni = self.carni
        self.update_fitness_sorted(herbi, self.h_parameters)
        self.update_fitness_sorted(carni, self.c_parameters)
        self.procreation(herbi, self.h_parameters, 'Herbivore')
        self.procreation(carni, self.c_parameters, 'Carnivore')
        return herbi, carni

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
        'Deletes animals with nagative fitness and fodder.'
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
        """
        Uses simple death function and updates herbi and carni
        with fewer animals after natural death
        """
        self.update_fitness_sorted(self.herbi, self.h_parameters)
        self.update_fitness_sorted(self.carni, self.c_parameters)
        self.death_function(self.carni, self.c_parameters)
        self.death_function(self.herbi, self.h_parameters)
        return self.herbi, self.carni

    def who_will_migrate(self, list_animal, parameter):
        """
        Make migration list as output from this function
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
        """
        Returns two lists, one for herbivores and one for carnivores, with
        animals that can migrate.
        """
        herbi_migration_list = self.who_will_migrate(self.herbi,
                                                     self.h_parameters)
        carni_migration_list = self.who_will_migrate(self.carni,
                                                     self.c_parameters)
        return herbi_migration_list, carni_migration_list

    def run_cell(self):
        """
        Method that runs Cell class. Outputs
        the modified input lists, list of migrating animals
        and fodder left in the cell.
        """
        food = self.feeding_herbi()
        updated_herbi = self.feeding_carni()
        self.herbi = updated_herbi
        herbi_born, carni_born = self.birth()
        self.herbi = herbi_born
        self.carni = carni_born
        self.age()
        self.weight_loss()
        herbi_new, carni_new = self.death()
        self.herbi = herbi_new
        self.carni = carni_new
        emigrators = self.send_out_emigrators()
        return self.herbi, self.carni, food, emigrators
