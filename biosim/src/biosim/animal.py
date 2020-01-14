# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

import math
import numpy as np


class Animal:


    def __init__(self, herbi_para, carni_para):

        self.herbi_para = herbi_para
        self.carni_para = carni_para


    def update_fitness_herbi(self, age, weight):

        if age < 0:
            raise ValueError("'age' must be non-negative")

        if weight <= 0:
            raise ValueError("'weight' must be positive")

        q_plus = (1 + math.e ** (self.herbi_para['phi_age']
                                 * (age - self.herbi_para['a_half'])))
        q_minus = (1 + math.e ** (-self.herbi_para['phi_weight']
                                  * (weight - self.herbi_para['w_half'])))
        self.fitness_herbi = (q_plus * q_minus) ** -1
        return (self.fitness_herbi)


    def update_fitness_carni(self, age, weight):

        if age < 0:
            raise ValueError("'age' must be non-negative")

        if weight <= 0:
            raise ValueError("'weight' must be positive")

        q_plus = (1 + math.e ** (self.carni_para['phi_age']
                                 * (age - self.carni_para['a_half'])))
        q_minus = (1 + math.e ** (-self.carni_para['phi_weight']
                                  * (weight - self.carni_para['w_half'])))
        self.fitness = (q_plus * q_minus) ** -1
        return (self.fitness)
