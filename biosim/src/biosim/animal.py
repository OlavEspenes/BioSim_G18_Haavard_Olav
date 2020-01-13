# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

import math
import numpy as np

class Animal:


    def __init__(self, age, weight, herbi_para, carni_para):

        if weight is None:
            self.weight = parameters['w_birth'] + np.random.normal()*parameters['sigma_birth']
        else:
            self.weight = weight

        self.age = age
        self.herbi_para = herbi_para
        self.carni_para = carni_para
        self.fitness = []

    def weight(self):
        return self.weight()

    def fitness_herbivores(self):
        q_plus = (1 + math.e ** (self.herbi_para['phi_age']
                                 * (self.age - self.herbi_para['a_half'])))
        q_minus = (1 + math.e ** (-self.herbi_para['phi_weight']
                                  * (self.weight - self.herbi_para['w_half'])))
        self.fitness = (q_plus * q_minus) ** -1
        return(self.fitness)

    def fitness_carnivores(self):
        q_plus = (1 + math.e ** (self.herbi_para['phi_age']
                                 * (self.age - self.herbi_para['a_half'])))
        q_minus = (1 + math.e ** (-self.herbi_para['phi_weight']
                                  * (self.weight - self.herbi_para['w_half'])))
        self.fitness = (q_plus * q_minus) ** -1
        return (self.fitness)
