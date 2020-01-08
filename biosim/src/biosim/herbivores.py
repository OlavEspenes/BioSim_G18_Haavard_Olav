# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

class Herbivores:
    default_h_parameters = {'w_birth': (8.0), 'sigma_birth': (4.0), 'beta': (0.9),
                  'eta': (0.05), 'a_half': (40.0), 'phi_age': (0.2),
                  'w_half': (10.0), 'phi_weight': (0.1), 'mu': (0.25),
                  'lambda': (1.0), 'gamma': (0.2), 'zeta': (3.5),
                  'xi': (1.2), 'omega': (0.4), 'F': (10.0)}
    h_parameters = copy.deepcopy(default_h_parameters)


@classmethod
def set_parameters(cls, choose_parameters):
    """
    :param cls:
    :param choose_parameters:
    :return:
    """
    for key in choose_parameters:
        if key in cls.h_parameters:
            if key is 'w_birth' or 'sigma_birth' or 'a_half' or 'w_half' or 







if __name__=="__main__":
    print(h_parameters)




