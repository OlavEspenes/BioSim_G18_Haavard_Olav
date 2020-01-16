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
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.ini_carni = []
        self.ini_herbi = []
        for i in self.ini_pop[1].get('pop'):
            if i.get('species') == 'Herbivore':
                self.herbi.append(i)
            elif i.get('species') == 'Carnivore':
                self.carni.append(i)
        self.landscape = Landscape()

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


    def where_to_migrate(self, migrator_list):
        mapsy = Landscape(self.island_map)
        mapsy.string_to_matrix()

    def string_to_matrix(self):
        """string made to nested list"""
        return [[i for i in j] for j in self.island.split()]

    def assign_tile(self):
        map = []
        for i, e in enumerate(self.string_to_matrix()):
            for j, n in enumerate(e):
                if n is 'O':
                    map.append(Ocean(i + 1, j + 1))
                elif n is 'J':
                    map.append(Jungle(i + 1, j + 1))
        return map

  #  [['O', 'O', 'O', 'K', 'K', 'O', 'O', 'O'],
  #  ['O', 'O', 'O', 'L', 'L', 'L', 'O', 'O'],
  #   ['O', 'O', 'O', 'O', 'L', 'O', 'O', 'O']]




    def simulation_one_year(self):
        h_para = landscape.h_parameters
        c_para = landscape.c_parameters
        rows = len(island)
        columns = len(island[1])
        fodder_island = [[None]*columns]*rows
        for row in rows:
            for col in columns:
                if island[row][columns] = 'S':
                fodder = fodder_island[row][columns] + 






    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """







        para = Landscape(self.island_map)
        cell = Cell(self.ini_herbi, self.ini_carni, fodder, herbi_para, carni_para, position))
        # Save lists in postitions.
        # go through one year on each position.
        for i in range(num_years):





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
