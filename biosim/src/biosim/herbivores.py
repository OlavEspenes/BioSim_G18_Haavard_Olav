# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

import math
import copy

class Herbivores:
    default_h_parameters = {'w_birth': 8.0,
                            'sigma_birth': 4.0,
                            'beta': 0.9,
                            'eta': 0.05,
                            'a_half': 40.0,
                            'phi_age': 0.2,
                            'w_half': 10.0,
                            'phi_weight': 0.1,
                            'mu': 0.25,
                            'lambda': 1.0,
                            'gamma': 0.2,
                            'zeta': 3.5,
                            'xi': 1.2,
                            'omega': 0.4,
                            'F': 10.0}
    parameters = copy.deepcopy(default_h_parameters)


    @classmethod
    def set_parameters(cls, choose_parameters):
    """
    :param cls:
    :param choose_parameters:
    :return:
    """
        for key in choose_parameters:
            if key in cls.parameters:
                if key is


    def __init__(self, age, weight):
        """

        :param self:
        :param age:
        :param weight:
        :return:
        """
        if age < 0:
            raise ValueError("Input value 'age' must be non-negative")
        else:
            self.age = age
        if weight <= 0:
            raise ValueError("Input value 'weight' must be positive")
        else:
            self.weight = weight

        self.fitness = None
        self.update_fitness()

    def update_fitness(self):
        """

        :param self:
        :return:
        """
        q_plus = (1 + e^(self.parameters['phi_age']
                         *(self.age - self.parameters['a_half'])))
        q_minus = (1 + e^(-self.parameters['phi_weight']
                          *(self.weight - self.parameters['w_half'])))
        









def __init__(self, age, weight):







if __name__=="__main__":
    print(h_parameters)




