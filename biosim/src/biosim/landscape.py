# -*- coding: utf-8 -*-

"""
"""

__author__ = "Olav Vikøren Espenes & Håvard Brobakken Eig"
__email__ = "olaves@nmbu.no, havardei@nmbu.no"


import copy
import numpy as np


class Landscape:
    """
    Method 
    """
    default_herbivores_para = {'w_birth': 8.0,
                               'sigma_birth': 1.5,
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

    default_carnivores_para = {'w_birth': 6.0,
                               'sigma_birth': 1.0,
                               'beta': 0.75,
                               'eta': 0.125,
                               'a_half': 60.0,
                               'phi_age': 0.4,
                               'w_half': 4.0,
                               'phi_weight': 0.4,
                               'mu': 0.4,
                               'lambda': 1.0,
                               'gamma': 0.8,
                               'zeta': 3.5,
                               'xi': 1.1,
                               'omega': 0.9,
                               'F': 50.0,
                               'DeltaPhiMax': 10.0}

    parameters = [copy.deepcopy(default_herbivores_para),
                  copy.deepcopy(default_carnivores_para)]

    default_jungle_parameters = {'f_max': 800.0}
    default_savannah_parameters = {'f_max': 300.0,
                                   'alpha': 0.3}

    landscape_parameters = [copy.deepcopy(default_jungle_parameters),
                            copy.deepcopy(default_savannah_parameters)]

    @classmethod
    def set_parameters_herbi(cls, herbi_para):

        """
        Method for users that want to set their own parameters for
        herbivore animals.

        Parameters
        ----------
        herbi_para : dictionary
            A dictionary with one or more keys to set new parameters for the
            animal. The items should be numeric.
        Raises
        ------
        KeyError
            When the dictionary with custom input parameters contain key(s)
            not already in the default parameters.
        ValueError
            When parameters in input dictionary are set to a value that are not
            valid to the norm for corresponding key.
        """
        for key in herbi_para:
            if key in cls.parameters[0]:
                if key is 'w_birth':
                    if herbi_para[key] < 0:
                        raise ValueError("'w_birth' must be positive")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'sigma_birth':
                    if herbi_para[key] < 0:
                        raise ValueError("'sigma_birth' must be positive")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'beta':
                    if 0 <= herbi_para[key] <= 1:
                        cls.parameters[0][key] = herbi_para[key]
                    else:
                        raise ValueError("'beta' must be in interval [0, 1]")

                elif key is 'eta':
                    if 0 <= herbi_para[key] <= 1:
                        cls.parameters[0][key] = herbi_para[key]
                    else:
                        raise ValueError("'eta' must be in interval [0, 1]")

                elif key is 'a_half':
                    if herbi_para[key] < 0:
                        raise ValueError("'a_half' must be positive")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'phi_age':
                    if herbi_para[key] < 0:
                        raise ValueError("'phi_age' must be positive")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'w_half':
                    if herbi_para[key] < 0:
                        raise ValueError("'w_half' must be positive")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'phi_weight':
                    if herbi_para[key] < 0:
                        raise ValueError("'phi_weight' must be positive")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'mu':
                    if herbi_para[key] < 0:
                        raise ValueError("'mu' must be positive")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'lambda':
                    if type(herbi_para[key]) is int or \
                            type(herbi_para[key]) is float:
                        cls.parameters[0][key] = herbi_para[key]
                    else:
                        raise ValueError("'lambda' must be a int or float")

                elif key is 'gamma':
                    if herbi_para[key] < 0:
                        raise ValueError("'gamma' must be positive")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'zeta':
                    if herbi_para[key] < 1:
                        raise ValueError("'zeta' must be greater than"
                                         " or equal to 1")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'xi':
                    if herbi_para[key] < 1:
                        raise ValueError("'xi' must be greater than"
                                         " or equal to 1")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'omega':
                    if herbi_para[key] < 0:
                        raise ValueError("'omega must be positive'")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                elif key is 'F':
                    if herbi_para[key] < 0:
                        raise ValueError("'F must be positive'")
                    else:
                        cls.parameters[0][key] = herbi_para[key]

                else:
                    pass
            else:
                raise KeyError(
                    "Your input is not a correct parameter key:'{0}'."
                    "Valid keys is found in Table 2, column 'Herb'." 
                    "; Column: 'Name'. Table 2 can be found in the"
                    "'Modelling the Ecosystem of Rossumøya' project"
                    "description".format(key))

    @classmethod
    def set_parameters_carni(cls, carni_para):
        for key in carni_para:
            if key in cls.parameters[1]:
                if key is 'w_birth':
                    if carni_para[key] < 0:
                        raise ValueError("'w_birth' must be positive")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'sigma_birth':
                    if carni_para[key] < 0:
                        raise ValueError("'sigma_birth' must be positive")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'beta':
                    if 0 <= carni_para[key] <= 1:
                        cls.parameters[1][key] = carni_para[key]
                    else:
                        raise ValueError("'beta' must be in interval [0, 1]")

                elif key is 'eta':
                    if 0 <= carni_para[key] <= 1:
                        cls.parameters[1][key] = carni_para[key]
                    else:
                        raise ValueError("'eta' must be in interval [0, 1]")

                elif key is 'a_half':
                    if carni_para[key] < 0:
                        raise ValueError("'a_half' must be positive")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'phi_age':
                    if carni_para[key] < 0:
                        raise ValueError("'phi_age' must be positive")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'w_half':
                    if carni_para[key] < 0:
                        raise ValueError("'w_half' must be positive")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'phi_weight':
                    if carni_para[key] < 0:
                        raise ValueError("'phi_weight' must be positive")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'mu':
                    if carni_para[key] < 0:
                        raise ValueError("'mu' must be positive")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'lambda':
                    if type(carni_para[key]) is int or \
                            type(carni_para[key]) is float:
                        cls.parameters[1][key] = carni_para[key]
                    else:
                        raise ValueError("'lambda' must be a int or float")

                elif key is 'gamma':
                    if carni_para[key] < 0:
                        raise ValueError("'gamma' must be positive")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'zeta':
                    if carni_para[key] < 1:
                        raise ValueError("'zeta' must be greater than"
                                         " or equal to 1")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'xi':
                    if carni_para[key] < 1:
                        raise ValueError("'xi' must be greater than"
                                         " or equal to 1")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'omega':
                    if carni_para[key] < 0:
                        raise ValueError("'omega must be positive'")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'F':
                    if carni_para[key] < 0:
                        raise ValueError("'F must be positive'")
                    else:
                        cls.parameters[1][key] = carni_para[key]

                elif key is 'DeltaPhiMax':
                    if carni_para[key] < 0:
                        raise ValueError("'DeltaPhiMax' must be positive")
                    else:
                        cls.parameters[1][key] = carni_para[key]
                else:
                    pass

            else:
                raise KeyError(
                    "Your input is not a correct parameter key:'{0}'."
                    "Valid keys is found in Table 2, column 'Carn'." 
                    "; Column: 'Name'. Table 2 can be found in the"
                    "'Modelling the Ecosystem of Rossumøya' project"
                    "description".format(key))

    @classmethod
    def set_jungle_parameters(cls, jungle_para):
        for key in jungle_para:
            if key in cls.landscape_parameters[0]:
                if key is 'f_max':
                    if jungle_para[key] < 0:
                        raise ValueError("'f_max' must be positive")
                    else:
                        cls.landscape_parameters[0][key] = jungle_para[key]
                else:
                    pass
            else:
                raise KeyError('You have entered wrong information')

    @classmethod
    def set_savannah_parameters(cls, savannah_para):
        for key in savannah_para:
            if key in cls.landscape_parameters[1]:
                if key is 'f_max':
                    if savannah_para[key] < 0:
                        raise ValueError("'f_max' must be positive")
                    else:
                        cls.landscape_parameters[1][key] = savannah_para[key]
                elif key is 'alpha':
                    if 1 <= savannah_para[key] <= 0:
                        raise ValueError("'alpha' must be between 0 and 1")
                    else:
                        cls.landscape_parameters[1][key] = savannah_para[key]
                else:
                    pass
            else:
                raise KeyError('You have entered wrong information')

    def __init__(self, island):
        self.island = island
        self.fodder = 0
        self.animal = []
        self.cells = None
        self.herbivores_on_island = None
        self.h_parameters = self.parameters[0]
        self.c_parameters = self.parameters[1]
        self.jungle_para = self.landscape_parameters[0]
        self.savannah_para = self.landscape_parameters[1]

    def make_fodder_island(self, island):
        fodder_map = [[i for i in j] for j in island.split()]
        for line in fodder_map:
            for index in range(len(fodder_map)):
                if len(fodder_map[index]) == len(line):
                    continue
                else:
                    raise ValueError('Map must have equal length for each row')
        c = np.array(fodder_map)
        edge = []
        edge += list(c[0, :])
        edge += list(c[-1, :])
        edge += list(c[1:-1, 0])
        edge += list(c[1:-1, -1])
        if set(edge) == {'O'}:
            pass
        else:
            raise SyntaxError('All edges must consist of only ocean!')

        fodder_map = [[[i] for i in j] for j in island.split()]
        for row, _ in enumerate(fodder_map):
            for col, _ in enumerate(fodder_map[0]):
                if fodder_map[row][col] == ['J']:
                    fodder_map[row][col].append(
                        self.jungle_para['f_max'])
                elif fodder_map[row][col] == ['S']:
                    fodder_map[row][col].append(
                        self.savannah_para['f_max'])
                elif fodder_map[row][col] == ['D']:
                    fodder_map[row][col].append(0)
                elif fodder_map[row][col] == ['O']:
                    fodder_map[row][col].append(0)
                elif fodder_map[row][col] == ['M']:
                    fodder_map[row][col].append(0)
                else:
                    raise ValueError('Use only letter J, S, D, O or M in map')
        return fodder_map

    def make_island_map(self, dim_map, ini_position, ini_herbi, ini_carni):
        if len(dim_map[0]) >= 1:
            island_map = [[[[], []] for i in range(len(dim_map[0]))] for j
                          in range(len(dim_map))]
        elif len(dim_map[1]) is True:
            island_map = [[[[], []] for i in range(len(dim_map[1]))] for j
                          in range(len(dim_map))]
        else:
            raise ValueError('No map given')

        for i in range(len(island_map)):
            for j in range(len(island_map[0])):
                if (i, j) == ini_position:
                    island_map[i][j][0] = ini_herbi
                    island_map[i][j][1] = ini_carni
        return island_map

    def set_pop(self, ini_pop):
        ini_carni = []
        ini_herbi = []
        ini_position = (0, 0)
        if ini_pop:
            for i, _ in enumerate(ini_pop[0]['pop']):
                if ini_pop[0]['pop'][i]['species'] == 'Herbivore':
                    ini_herbi.append(ini_pop[0]['pop'][i])
                elif ini_pop[0]['pop'][i]['species'] == 'Carnivore':
                    ini_herbi.append(ini_pop[0]['pop'][i])
                else:
                    raise ValueError('Something about the input is wrong')
            ini_position = ini_pop[0]['loc']
        return ini_herbi, ini_carni, ini_position
