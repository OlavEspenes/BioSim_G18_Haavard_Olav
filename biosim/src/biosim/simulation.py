# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

from cell import Cell
from landscape import Landscape

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
        self.ini_position = ini_pop[0].get('loc')
        ini_carni = []
        ini_herbi = []
        for i in ini_pop[1].get('pop'):
            if i.get('species') == 'Herbivore':
                ini_herbi.append(i)
            elif i.get('species') == 'Carnivore':
                ini_carni.append(i)
        self.landscape = Landscape()
        self.fodder_map = [[[i] for i in j] for j in island_map.split()]

        for row in range(len(self.fodder_map)):
            for col in range(len(self.fodder_map[1])):
                if self.fodder_map[row][col] == ['J']:
                    self.fodder_map[row][col].append(self.landscape.jungle_para['f_max']) #må endres!!!111!
                if self.fodder_map[row][col] == ['S']:
                    self.fodder_map[row][col].append(self.landscape.savannah_para['f_max'])
                if self.fodder_map[row][col] == ['D']:
                    self.fodder_map[row][col].append(0)

        self.island_map = [[None for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))]
        for i in range(len(self.island_map)): #put input pop in
            for j in range(len(self.island_map[0])):
                if (i, j) == self.ini_position:
                    self.island_map[i][j] = [ini_herbi, ini_carni]

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

    def append_emigrators(self, list_carni, list_herbi, position):
        for i in range(len(self.island_map)):
            for j in range(len(self.island_map[0])):
                if (i, j) == position:
                    if self.island_map[i][j] is None:
                        self.island_map[i][j] = [list_herbi, list_carni]
                    elif self.island_map[i][j] is not None:
                        self.island_map[i][j][0] += list_herbi
                        self.island_map[i][j][1] += list_carni


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


    def where_to_migrate(self, migrator_list):
        pass


    #  [['O', 'O', 'O', 'K', 'K', 'O', 'O', 'O'],
    #  ['O', 'O', 'O', 'L', 'L', 'L', 'O', 'O'],
    #   ['O', 'O', 'O', 'O', 'L', 'O', 'O', 'O']]




    def simulation_one_year(self):
        h_para = self.landscape.h_parameters
        c_para = self.landscape.c_parameters
        rows = len(self.fodder_map)
        columns = len(self.fodder_map[1])
        herbi_migration = [[None]*columns]*rows
        carni_migration = [[None]*columns]*rows

        for row in range(rows):
            for col in range(columns):
                if self.fodder_map[row][col] is not None:
                    herbi = herbi_map[row][col]
                    carni = carni_map[row][col]
                    fodder = self.fodder_map[row][col]
                    cell = Cell(herbi, carni, fodder, h_para, c_para)
                    cell.feeding_herbi()
                    cell.feeding_carni()
                    cell.birth()
                    cell.age()
                    cell.weight_loss()
                    cell.death()
                    emigrations = send_out_emigrators()
                    herbivores[row][col] = cell.herbi
                    carnivores[row][col] = cell.carni
                    herbi_migration[row][col] = emigrations[0]
                    carni_migration[row][col] = emigrations[1]


                neighbors_cells = []
                epsilon






    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """


        for year in num_years:




        for i in range(num_years):
            self.simulation_one_year()



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

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
