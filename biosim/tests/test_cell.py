# -*- coding: utf-8 -*-

"""

"""

__author__ = "Olav Vikøren Espenes & Håvard Brobakken Eig"
__email__ = "olaves@nmbu.no, havardei@nmbu.no"

from biosim.cell import Cell
import pytest
import random


class TestCell:
    @pytest.fixture()
    def create_animals(self):
        self.herbi = [{'species': 'Herbivore', 'age': 3, 'weight': 20},
                      {'species': 'Herbivore', 'age': 4, 'weight': 50},
                      {'species': 'Herbivore', 'age': 2, 'weight': 10},
                      {'species': 'Herbivore', 'age': 1, 'weight': 5}]
        self.carni = [{'species': 'Carnivore', 'age': 20, 'weight': 100},
                      {'species': 'Carnivore', 'age': 15, 'weight': 200}]
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

    def test_fitness_single_animal(self):
        """
        Checks that animal with slightly greater
        weight has better fitness and that its
        between 0 and 1.
        """
        self.create_animals()
        ani_one = self.cell.fitness_single_animal(3, 10, self.h_parameter)
        ani_two = self.cell.fitness_single_animal(3, 11, self.h_parameter)
        assert ani_one < ani_two
        assert 0 < ani_one < 1
        assert 0 < ani_two < 1

    def test_update_fitness_sorted(self):
        """
        Checks that animals is sorted by fitness
        from highest to lowest.
        """
        self.create_animals()
        self.cell.update_fitness_sorted(self.herbi, self.h_parameter)
        assert self.herbi[0].get('fitness') > self.herbi[1].get('fitness')
        assert self.herbi[1].get('fitness') > self.herbi[2].get('fitness')

    def test_feeding_herbi(self):
        """
        Checks that its less fodder after eating.
        """
        self.create_animals()
        after_feed = self.cell.feeding_herbi()
        assert self.fodder > after_feed

    def test_feeding_herbi_negative_fodder(self):
        """
        Checks that ValueError is raised
        when fodder is below 0
        """
        self.create_animals()
        with pytest.raises(ValueError):
            cell = Cell(self.herbi, self.carni, -1,
                             self.h_parameter, self.c_parameter)
            cell.feeding_herbi()

    def test_feeding_herbi_no_fodder(self):
        """
        Checks that animals is not fed when there's no fodder.
        """
        random.seed(42)
        self.create_animals()
        cell2 = Cell(self.herbi, self.carni, 0, self.h_parameter, self.c_parameter)
        cell2.feeding_herbi()
        assert self.herbi[0].get('weight') == 50

    def test_feeding_herbi_eat_less_than_appetite(self):
        random.seed(42)
        self.create_animals()
        cell2 = Cell(self.herbi, self.carni, 3, self.h_parameter,
                     self.c_parameter)
        fodder = cell2.feeding_herbi()
        assert self.herbi[0].get('weight') > 50
        assert fodder == 0

    def test_feeding_carni(self):
        """
        Checks that at least one herivore has been eaten.
        """
        random.seed(134)
        self.create_animals()
        self.cell.feeding_carni()
        assert len(self.herbi) < 4

    def test_procreation(self):
        """
        Checks that there have been added at least one child.
        Also checks that child's age is 0.
        """
        random.seed(190923)
        self.create_animals()
        self.cell.procreation(self.herbi, self.h_parameter, 'Herbivore')
        assert len(self.herbi) > 4
        assert self.herbi[4].get('age') == 0

    def test_age(self):
        """
        Checks that one year have been added to age.
        """
        self.create_animals()
        self.cell.age()
        assert self.herbi[0]['age'] == 4

    def test_weight_loss(self):
        """
        Checks that weight have become less.
        """
        self.create_animals()
        self.cell.weight_loss()
        assert self.herbi[0].get('weight') < 20

    def test_death_function(self):
        """
        Checks that at least one herbivore has been killed off.
        """
        random.seed(425)
        self.create_animals()
        self.cell.death_function(self.herbi, self.h_parameter)
        assert len(self.herbi) < 4

    def test_death_function_negative_fitness(self):
        """
        Checks that animal with 0 weight and fitness i killed.
        """
        self.create_animals()
        herbivore = [{'species': 'Herbivore', 'age': 0, 'weight': 0}]
        self.cell.death_function(herbivore, self.h_parameter)
        assert len(herbivore) == 0

    def test_who_will_migrate(self):
        """
        Checks that it's at least one less herbivore and
        one migrant. Also that the combined amount og animals
        is the same at before the migration.
        """
        random.seed(1234)
        self.create_animals()
        emigrant = self.cell.who_will_migrate(self.herbi, self.h_parameter)
        assert len(self.herbi) < 4
        assert len(emigrant) > 0
        assert len(self.herbi) + len(emigrant) == 4

    def test_run_cell(self):
        self.create_animals()
        self.cell.run_cell()
