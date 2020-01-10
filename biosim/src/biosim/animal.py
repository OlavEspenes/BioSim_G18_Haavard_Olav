# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

class Animal:


    def __init__(self, species, age, weight, parameters):

    if weight is None:
        self.weight = parameters['w_birth'] + np.random.normal()*parameters['sigma_birth']
    else:
        self.weight = weight

    def fitness(self, ):
            q_plus = (1 + math.e ** (parameters['phi_age']
                                     * (i['age'] - parameters['a_half'])))
            q_minus = (1 + math.e ** (-parameters['phi_weight']
                                      * (i['weight'] - parameters['w_half'])))
            i['fitness'] = (q_plus * q_minus) ** -1

