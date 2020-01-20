# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

import math
from cell import Cell
from landscape import Landscape
import random

class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        random.seed(seed)
        self.ini_position = ini_pop[0].get('loc')
        ini_carni = []
        ini_herbi = []
        for i in ini_pop[1].get('pop'):
            if i.get('species') == 'Herbivore':
                ini_herbi.append(i)
            elif i.get('species') == 'Carnivore':
                ini_carni.append(i)
        self.landscape = Landscape(island_map)

        self.fodder_map = [[[i] for i in j] for j in island_map.split()]
        for row, _ in enumerate(self.fodder_map):
            for col, _ in enumerate(self.fodder_map[0]):
                if self.fodder_map[row][col] == ['J']:
                    self.fodder_map[row][col].append(self.landscape.jungle_para['f_max'])
                if self.fodder_map[row][col] == ['S']:
                    self.fodder_map[row][col].append(self.landscape.savannah_para['f_max'])
                if self.fodder_map[row][col] == ['D']:
                    self.fodder_map[row][col].append(0)
                if self.fodder_map[row][col] == ['O']:
                    self.fodder_map[row][col].append(0)
                if self.fodder_map[row][col] == ['M']:
                    self.fodder_map[row][col].append(0)

        self.island_map = [[[None, None] for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))] ## HUSK Å LEGGE INN TOM LISTE
        for i in range(len(self.island_map)):
            for j in range(len(self.island_map[0])):
                if (i, j) == self.ini_position:
                    self.island_map[i][j][0] = ini_herbi
                    self.island_map[i][j][1] = ini_carni

        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Herbivores':
            landscape.set_parameters_herbi(params)
        elif species == 'Carnivores':
            landscape.set_parameters_carni(params)
        else:
            raise ValueError("'species' must be Herbivores or Carnivores")


    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'J':
            landscape.set_jungle_parameters(params)
        elif landscape == 'S':
            landscape.set_savannah_parameters(params)
        else:
            raise ValueError("'landscape' must be 'J' (Jungel) "
                             "or 'S' (savannah)")

    def simulation_one_year(self):
        h_para = self.landscape.h_parameters
        c_para = self.landscape.c_parameters
        rows = len(self.fodder_map)
        columns = len(self.fodder_map[1])
        herbi_migration = [[None for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))]
        carni_migration = [[None for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))]
        migrated_herbi = [[[None] for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))]
        migrated_carni = [[[None] for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))]
        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):
                if self.island_map[row][col][0] is not None:
                    herbi = self.island_map[row][col][0]
                    carni = self.island_map[row][col][1]
                    fodder = self.fodder_map[row][col][1]
                    cell = Cell(herbi, carni, fodder, h_para, c_para)
                    cell.feeding_herbi()
                    cell.feeding_carni()
                    cell.birth()
                    cell.age()
                    cell.weight_loss()
                    cell.death()
                    emigrations = cell.send_out_emigrators()
                    herbi_migration[row][col] = emigrations[0]
                    carni_migration[row][col] = emigrations[1]
                    self.fodder_map[row][col][1] = cell.fodder

        # Migration herbivores
        if not herbi_migration:
            pass
        else:
            for row, _ in enumerate(herbi_migration):
                for col, _ in enumerate(herbi_migration[0]):
                    if herbi_migration[row][col] is None:
                        continue
                    else:
                        for h_migrant, _ in enumerate(herbi_migration[row][col]):
                            north_f = self.fodder_map[row-1][col][1]
                            east_f = self.fodder_map[row][col+1][1]
                            south_f = self.fodder_map[row+1][col][1]
                            west_f = self.fodder_map[row][col-1][1]
                            if self.island_map[row-1][col][0] is None:
                                epsilon_north = north_f/(1*h_para['F'])
                            else:
                                epsilon_north = north_f/(len(self.island_map[row-1][col][0])+1)*h_para['F']
                            if self.island_map[row][col+1][0] is None:
                                epsilon_east = east_f/(1*h_para['F'])
                            else:
                                epsilon_east = east_f/(len(self.island_map[row][col+1][0])+1)*h_para['F']
                            if self.island_map[row+1][col][0] is None:
                                epsilon_south = south_f / (1*h_para['F'])
                            else:
                                epsilon_south = south_f/(len(self.island_map[row+1][col][0])+1)*h_para['F']
                            if self.island_map[row][col-1][0] is None:
                                epsilon_west = west_f / (1*h_para['F'])
                            else:
                                epsilon_west = west_f/(len(self.island_map[row][col-1][0])+1)*h_para['F']

                            if self.fodder_map[row-1][col][0] == 'M' or \
                                    self.fodder_map[row-1][col][0] == 'O':
                                propensity_north = 0
                            else:
                                propensity_north = math.exp(h_para['lambda']*epsilon_north)
                            if self.fodder_map[row][col+1][0] == 'M' or \
                                    self.fodder_map[row][col+1][0] == 'O':
                                propensity_east = 0
                            else:
                                propensity_east = math.exp(h_para['lambda']*epsilon_east)
                            if self.fodder_map[row+1][col][0] == 'M' or \
                                    self.fodder_map[row+1][col][0] == 'O':
                                propensity_south = 0
                            else:
                                propensity_south = math.exp(h_para['lambda']*epsilon_south)
                            if self.fodder_map[row][col-1][0] == 'M' or \
                                    self.fodder_map[row][col-1][0] == 'O':
                                propensity_west = 0
                            else:
                                propensity_west = math.exp(h_para['lambda']*epsilon_west)

                            propensity_tot = propensity_north+propensity_east+propensity_south+propensity_west
                            probability_north = propensity_north / propensity_tot
                            probability_east = propensity_east / propensity_tot
                            probability_south = propensity_south / propensity_tot
                            probability_west = propensity_west / propensity_tot
                            probability_not_to_move = 1 - probability_north - probability_east - probability_south - probability_west

                            choosen_cell = random.choices(['move_north',
                                                           'move_east',
                                                           'move_south',
                                                           'move_west',
                                                           'not_move'],
                                                          weights=
                                                          [probability_north,
                                                           probability_east,
                                                           probability_south,
                                                           probability_west,
                                                           probability_not_to_move])
                            if choosen_cell == ['move_north']:
                                migrated_herbi[row - 1][col] += herbi_migration[row][col]
                            elif choosen_cell == ['move_east']:
                                migrated_herbi[row][col + 1] += herbi_migration[row][col]
                            elif choosen_cell == ['move_south']:
                                migrated_herbi[row+1][col] += herbi_migration[row][col]
                            elif choosen_cell == ['move_west']:
                                migrated_herbi[row][col - 1] += herbi_migration[row][col]
                            elif choosen_cell == ['stay']:
                                migrated_herbi[row][col] += herbi_migration[row][col]

        















        if not carni_migration:
            pass
        else:
            for row, _ in enumerate(carni_migration):
                for col, _ in enumerate(carni_migration[0]):
                    if carni_migration[row][col] is None:
                        continue
                    else:
                        for c_migrant in enumerate(carni_migration[row][col]):
                            north_f = 0
                            east_f = 0
                            south_f = 0
                            west_f = 0
                            for h,_ in enumerate(self.island_map[row-1][col][0]):
                                north_f += self.island_map[row-1][col][0][h]['weight']
                            for h,_ in enumerate(self.island_map[row][col+1][0]):
                                east_f += self.island_map[row][col+1][0][h]['weight']
                            for h,_ in enumerate(self.island_map[row+1][col][0]):
                                south_f += self.island_map[row+1][col][0][h]['weight']
                            for h,_ in enumerate(self.island_map[row][col-1][0]):
                                west_f += self.island_map[row][col-1][0][h]['weight']

                            epsilon_north = north_f/(len(self.island_map[row-1][col][1])+1)*c_para['F']
                            epsilon_east = east_f/(len(self.island_map[row][col+1][1])+1)*c_para['F']
                            epsilon_south = south_f/(len(self.island_map[row+1][col][1])+1)*c_para['F']
                            epsilon_west = west_f/(len(self.island_map[row][col-1][1]+1))*c_para['F']


                            if self.fodder_map[row-1][col][0] == 'M' or \
                                    self.fodder_map[row-1][col][0] == 'O']:
                                propensity_north = 0
                            else:
                                propensity_north = math.exp(c_para['lambda']*epsilon_north)
                            if self.fodder_map[row][col+1][0] == 'M' or \
                                    self.fodder_map[row][col+1][0] == 'O':
                                propensity_east = 0
                            else:
                                propensity_east = math.exp(c_para['lambda']*epsilon_east)
                            if self.fodder_map[row+1][col][0] == 'M' or \
                                    self.fodder_map[row+1][col][0] == 'O':
                                propensity_south = 0
                            else:
                                propensity_south = math.exp(c_para['lambda']*epsilon_south)
                            if self.fodder_map[row][col-1][0] == 'M' or \
                                    self.fodder_map[row][col-1][0] == 'O':
                                propensity_west = 0
                            else:
                                propensity_west = math.exp(c_para['lambda']*epsilon_west)


                            propensity_tot = propensity_north+propensity_east+propensity_south+propensity_west

                            probability_north = propensity_north / propensity_tot
                            probability_east = propensity_east / propensity_tot
                            probability_south = propensity_south / propensity_tot
                            probability_west = propensity_west / propensity_tot
                            probability_not_to_move = 1 - probability_north - propensity_east - propensity_south - propensity_west

                            choosen_cell = random.choices(['move_north',
                                                           'move_east',
                                                           'move_south',
                                                           'move_west',
                                                           'not_move'],
                                                          weights =
                                                          [probability_north,
                                                           probability_east,
                                                           probability_south,
                                                           probability_west,
                                                           probability_not_to_move])
                            if choosen_cell == ['move_north']:
                                migrated_carni[row-1][col] += carni_migration[row][col]
                            elif choosen_cell == ['move_east']:
                                migrated_carni[row][col+1] += carni_migration[row][col]
                            elif choosen_cell == ['move_south']:
                                migrated_carni[row+1][col] += carni_migration[row][col]
                            elif choosen_cell == ['move_west']:
                                migrated_carni[row][col-1] += carni_migration[row][col]
                            elif choosen_cell == ['stay']:
                                migrated_carni[row][col] += carni_migration[row][col]




    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """


        #for year in num_years:
        #for i in range(num_years):
        #    self.simulation_one_year()
    pass


    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        pass


    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

        for h,_ in enumerate

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
