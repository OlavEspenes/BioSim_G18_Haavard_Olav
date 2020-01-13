
import copy
import numpy as np


class Landscape:


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

    parameters = [copy.deepcopy(default_herbivores_para), copy.deepcopy(default_carnivores_para)


    @classmethod
    def set_parameters_herbi(cls, herbi_para):

        """
        Method for users that want to set their own parameters for
        herbivore animals.

        Parameters
        ----------
        parameter_changes : dictionary
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


    def __init__(self, island):
        self.island = island
        self.fodder = 0
        self.animal = []
        self.cells = None
        self.herbivores_on_island = None

    def string_to_matrix(self):
        """string made to nested list"""
        temp = copy.deepcopy(self.island.replace(" ", ""))
        list_map = [[i for i in j] for j in temp.split()]
        return list_map

    """
    def array_cont(self):
        listed_map = self.string_to_matrix()
        array_shape = np.shape(listed_map)

        nested = list(np.zeros(array_shape))
        for i, e in enumerate(nested):
            nested[i] = list(e)

        self.cells = np.array(nested)
    """

    def assign_tile(self):
        self.kart = []
        for i, e in enumerate(self.string_to_matrix()):
            for j, n in enumerate(e):
                if n is 'O':
                    self.kart.append(Ocean(i+1, j+1))
                elif n is 'J':
                    self.kart.append(Jungle(i+1, j+1))
        return self.kart


    def fodder_added(self):
        pass

    def fodder_decreased(self):
        pass

    def animals(self):
        pass







