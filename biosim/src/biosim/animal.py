# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

class Animal:


    def __init__(self, age, weight, parameters):

        if weight is None:
            self.weight = parameters['w_birth'] + np.random.normal()*parameters['sigma_birth']
        else:
            self.weight = weight

        self.age = age

        q_plus = (1 + math.e ** (parameters['phi_age']
                                     * (self.age - parameters['a_half'])))
        q_minus = (1 + math.e ** (-parameters['phi_weight']
                                      * (self.weight - parameters['w_half'])))
        fitness = (q_plus * q_minus) ** -1
        print(fitness)

