# -*- coding: utf-8 -*-

"""

"""

__author__ = "Olav Vikøren Espenes & Håvard Brobakken Eig"
__email__ = "olaves@nmbu.no, havardei@nmbu.no"

from biosim.cell import Cell
import pytest

class TestCell:
    @pytest.fixture()
    def create_animals(self):
        self.herbi = [{'species': 'Herbivore', 'age': 3, 'weight': 20},
                      {'species': 'Herbivore', 'age': 4, 'weight': 50}]
        self.carni = [{'species': 'Carnivore', 'age': 3, 'weight': 20},
                      {'species': 'Carnivore', 'age': 3, 'weight': 20}]
        self.h_parameter = {'w_birth': 8.0,
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
        self.c_parameter = {'w_birth': 6.0,
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
        self.fodder = 800
        self.cell = Cell(self.herbi, self.carni, self.fodder, self.h_parameter, self.c_parameter)


    def test_cell(self):
        pass

    def test_fitness_single_animal(self):
        """
        Checks that animal with slightly greater
        weight has better fitness
        """
        self.create_animals()
        ani_one = self.cell.fitness_single_animal(3, 10, self.h_parameter)
        ani_two = self.cell.fitness_single_animal(3, 11, self.h_parameter)
        assert ani_one < ani_two

    def test_update_fitness_sorted(self):
        """
        Checks that
        """
        self.create_animals()
        self.cell.update_fitness_sorted(self.herbi, self.h_parameter)
        assert self.herbi[0].get('fitness') < self.herbi[1].get('fitness')

    def test_feeding_herbi(self):
        pass

    def test_feeding_carni(self):
        pass

    def test_age(self):
        self.create_animals()
        self.cell.age()
        assert self.herbi[0].get('age') == 4

