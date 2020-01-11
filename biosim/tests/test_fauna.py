# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

import random
from animal import Animal

def test_no_weight_animal():
    test_parameters = {'w_birth': 8.0,
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
    one_hurbivore = {'species': 'Herbivore', 'age': 2, 'weight': 60}
    age = random.randrange(10)
    weight = None
    test = Animal(age, weight, test_parameters)


def test_age():







def test_update_fitness():
