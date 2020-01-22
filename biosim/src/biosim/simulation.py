# -*- coding: utf-8 -*-

"""
"""

__author__ = "Olav Vikøren Espenes & Håvard Brobakken Eig"
__email__ = "olaves@nmbu.no, havardei@nmbu.no"

import math
from biosim.cell import Cell
from biosim.landscape import Landscape
import random
import pandas as pd
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import subprocess
import os
import textwrap

_FFMPEG_BINARY = r'C:/Users/olav9/' \
                 r'OneDrive - Norwegian University of Life Sciences/' \
                 r'Documents/NMBU/H2019/INF200/' \
                 r'ffmpeg-20200115-0dc0837-win64-static/' \
                 r'ffmpeg-20200115-0dc0837-win64-static/bin/ffmpeg'

DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
DEFAULT_GRAPHICS_NAME = 'dv'
DEFAULT_MOVIE_FORMAT = 'mp4'


class BioSim:
    def __init__(self, island_map, ini_pop, seed, ymax_animals=None,
                 cmax_animals=None, img_base=None, img_fmt="png"):

        random.seed(seed)
        self.landscape = Landscape(island_map)
        ini_herbi, ini_carni, ini_position = self.landscape.set_pop(ini_pop)
        self.fodder_map = self.landscape.make_fodder_island(island_map)
        self.island_map = self.landscape.make_island_map(self.fodder_map,
                                                         ini_position,
                                                         ini_herbi, ini_carni)

        self.total_count_herbi = 0
        self.total_count_carni = 0
        self.island_string = island_map
        self.ymax_animals = ymax_animals
        self._year = 0
        self._final_year = None
        self.img_fmt = img_fmt
        self.img_ctr = 0
        if img_base is None:
            self.img_base = os.path.join('..', 'BioSim')
        if cmax_animals is None:
            self.cmax_animals = {}

        self.total_pop_herbi = 0
        self.total_pop_carni = 0

        self.fig = None
        self.ax_year = None
        self.ax_map = None
        self.ax_line = None
        self.ax_heat_h = None
        self.ax_heat_c = None
        self.h_density = None
        self.c_density = None
        self.y_label_h = []
        self.y_label_c = []
        self.line_herb = None
        self.line_carn = None
        self.year_plot = None
        self.map_geo = None
        self.animal_dis = None
        self.herbi_migration = [[[] for i in range(len(self.fodder_map[1]))]
                                for j in range(len(self.fodder_map))]
        self.carni_migration = [[[] for i in range(len(self.fodder_map[1]))]
                                for j in range(len(self.fodder_map))]
        self.migrated_herbi = [[[] for i in range(len(self.fodder_map[1]))]
                               for j in range(len(self.fodder_map))]
        self.migrated_carni = [[[] for i in range(len(self.fodder_map[1]))]
                               for j in range(len(self.fodder_map))]

        """
        :param island_map: Multi-line string specifying island geography.
        :param ini_pop: List of dictionaries specifying initial population.
        :param seed: Integer used as random number seed.
        :param ymax_animals: Number specifying y-axis limit for graph showing
                animal numbers.
        :param cmax_animals: Dict specifying color-code limits for
                animal densities.
        :param img_base: String with beginning of file name for figures, 
                including path.
        :param img_fmt: String with file type for figures, e.g. 'png'.

        If ymax_animals is None, the y-axis limit should be adjusted 
            automatically.

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
        if species == 'Herbivore':
            self.landscape.set_parameters_herbi(params)
        elif species == 'Carnivore':
            self.landscape.set_parameters_carni(params)
        else:
            raise ValueError("species' must be Herbivores or Carnivores")

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'J':
            self.landscape.set_jungle_parameters(params)
        elif landscape == 'S':
            self.landscape.set_savannah_parameters(params)
        else:
            raise ValueError("'landscape' must be 'J' (Jungel) "
                             "or 'S' (savannah)")

    def simulation_one_year(self):
        h_para = self.landscape.h_parameters
        c_para = self.landscape.c_parameters

        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):
                if self.island_map[row][col][0] is not None or \
                        self.island_map[row][col][1] is not None:
                    herbi = self.island_map[row][col][0]
                    carni = self.island_map[row][col][1]

                    # Grow fodder
                    if self.fodder_map[row][col][0] == 'J':
                        fodder = self.landscape.jungle_para['f_max']
                    elif self.fodder_map[row][col][0] == 'S':
                        fodder = self.fodder_map[row][col][1] \
                                 + self.landscape.savannah_para['alpha'] \
                                 * (self.landscape.savannah_para['f_max']
                                    - self.fodder_map[row][col][1])
                    else:
                        fodder = self.fodder_map[row][col][1]

                    cell = Cell(herbi, carni, fodder, h_para, c_para)
                    herbi, carni, food, emigrators = cell.run_cell()
                    self.island_map[row][col][1] = carni
                    self.island_map[row][col][0] = herbi
                    self.herbi_migration[row][col] = emigrators[0]
                    self.carni_migration[row][col] = emigrators[1]
                    self.fodder_map[row][col][1] = food

    def migrate_herbivores(self):
        h_para = self.landscape.h_parameters
        if not self.herbi_migration:
            pass
        else:
            for row, _ in enumerate(self.herbi_migration):
                for col, _ in enumerate(self.herbi_migration[0]):
                    if self.herbi_migration[row][col] is None:
                        continue
                    else:
                        for h_migrant, _ in enumerate(
                                self.herbi_migration[row][col]):
                            north_f = self.fodder_map[row - 1][col][1]
                            east_f = self.fodder_map[row][col + 1][1]
                            south_f = self.fodder_map[row + 1][col][1]
                            west_f = self.fodder_map[row][col - 1][1]
                            if not self.island_map[row - 1][col][0]:
                                epsilon_north = north_f / (1 * h_para['F'])
                            else:
                                epsilon_north = north_f / (len(
                                    self.island_map[row - 1][col][0]) + 1) * \
                                                h_para['F']
                            if not self.island_map[row][col + 1][0]:
                                epsilon_east = east_f / (1 * h_para['F'])
                            else:
                                epsilon_east = east_f / (len(
                                    self.island_map[row][col + 1][0]) + 1) * \
                                               h_para['F']
                            if not self.island_map[row + 1][col][0]:
                                epsilon_south = south_f / (1 * h_para['F'])
                            else:
                                epsilon_south = south_f / (len(
                                    self.island_map[row + 1][col][0]) + 1) * \
                                                h_para['F']
                            if not self.island_map[row][col - 1][0]:
                                epsilon_west = west_f / (1 * h_para['F'])
                            else:
                                epsilon_west = west_f / (len(
                                    self.island_map[row][col - 1][0]) + 1) * \
                                               h_para['F']

                            if self.fodder_map[row - 1][col][0] == 'M' or \
                                    self.fodder_map[row - 1][col][0] == 'O':
                                propensity_north = 0
                            else:
                                if epsilon_north > 600:
                                    epsilon_north = 600
                                propensity_north = math.exp(
                                    h_para['lambda'] * epsilon_north)
                            if self.fodder_map[row][col + 1][0] == 'M' or \
                                    self.fodder_map[row][col + 1][0] == 'O':
                                propensity_east = 0
                            else:
                                if epsilon_east > 600:
                                    epsilon_east = 600
                                propensity_east = math.exp(
                                    h_para['lambda'] * epsilon_east)
                            if self.fodder_map[row + 1][col][0] == 'M' or \
                                    self.fodder_map[row + 1][col][0] == 'O':
                                propensity_south = 0
                            else:
                                if epsilon_south > 600:
                                    epsilon_south = 600
                                propensity_south = math.exp(
                                    h_para['lambda'] * epsilon_south)
                            if self.fodder_map[row][col - 1][0] == 'M' or \
                                    self.fodder_map[row][col - 1][0] == 'O':
                                propensity_west = 0
                            else:
                                if epsilon_west > 600:
                                    epsilon_west = 600
                                propensity_west = math.exp(
                                    h_para['lambda'] * epsilon_west)

                            propensity_tot = \
                                propensity_north + propensity_east + \
                                propensity_south + propensity_west

                            if propensity_tot == 0:
                                probability_north = 0
                                probability_east = 0
                                probability_south = 0
                                probability_west = 0
                            else:
                                probability_north = \
                                    propensity_north / propensity_tot
                                probability_east = \
                                    propensity_east / propensity_tot
                                probability_south = \
                                    propensity_south / propensity_tot
                                probability_west = \
                                    propensity_west / propensity_tot
                            probability_not_to_move = \
                                1 - probability_north - probability_east - \
                                probability_south - probability_west

                            choosen_cell =\
                                random.choices(
                                    ['move_north', 'move_east', 'move_south',
                                     'move_west', 'not_move'],
                                    weights=[probability_north,
                                             probability_east,
                                             probability_south,
                                             probability_west,
                                             probability_not_to_move])
                            if choosen_cell == ['move_north']:
                                self.migrated_herbi[row - 1][col] += \
                                    self.herbi_migration[row][col]
                            elif choosen_cell == ['move_east']:
                                self.migrated_herbi[row][col + 1] += \
                                    self.herbi_migration[row][col]
                            elif choosen_cell == ['move_south']:
                                self.migrated_herbi[row + 1][col] += \
                                    self.herbi_migration[row][col]
                            elif choosen_cell == ['move_west']:
                                self.migrated_herbi[row][col - 1] += \
                                    self.herbi_migration[row][col]
                            elif choosen_cell == ['stay']:
                                self.migrated_herbi[row][col] += \
                                    self.herbi_migration[row][col]

        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):
                if not self.migrated_herbi[row][col]:
                    continue
                else:
                    self.island_map[row][col][0] \
                        += self.migrated_herbi[row][col]

    def migrate_carnivores(self):
        c_para = self.landscape.c_parameters
        if not self.carni_migration:
            pass
        else:
            for row, _ in enumerate(self.carni_migration):
                for col, _ in enumerate(self.carni_migration[0]):
                    if self.carni_migration[row][col] is None:
                        continue
                    else:
                        for c_migrant, _ in enumerate(
                                self.carni_migration[row][col]):
                            north_f = 0
                            east_f = 0
                            south_f = 0
                            west_f = 0
                            for h in range(
                                    len(self.island_map[row - 1][col][0])):
                                north_f += self.island_map[row - 1][col][0][h][
                                    'weight']
                            for h in range(
                                    len(self.island_map[row][col + 1][0])):
                                east_f += self.island_map[row][col + 1][0][h][
                                    'weight']
                            for h in range(
                                    len(self.island_map[row + 1][col][0])):
                                south_f += self.island_map[row + 1][col][0][h][
                                    'weight']
                            for h in range(
                                    len(self.island_map[row][col - 1][0])):
                                west_f += self.island_map[row][col - 1][0][h][
                                    'weight']

                            epsilon_north = north_f / (len(
                                self.island_map[row - 1][col][1])
                                                       + 1)*c_para['F']
                            epsilon_east = east_f / (len(
                                self.island_map[row][col + 1][1])
                                                     + 1)*c_para['F']
                            epsilon_south = south_f / (len(
                                self.island_map[row + 1][col][1])
                                                       + 1)*c_para['F']
                            epsilon_west = west_f / (len(
                                self.island_map[row][col - 1][1])
                                                     + 1)*c_para['F']

                            if self.fodder_map[row - 1][col][0] == 'M' or \
                                    self.fodder_map[row - 1][col][0] == 'O':
                                propensity_north = 0
                            else:
                                if epsilon_north > 600:
                                    epsilon_north = 600
                                propensity_north = math.exp(
                                    c_para['lambda'] * epsilon_north)
                            if self.fodder_map[row][col + 1][0] == 'M' or \
                                    self.fodder_map[row][col + 1][0] == 'O':
                                propensity_east = 0
                            else:
                                if epsilon_east > 600:
                                    epsilon_east = 600
                                propensity_east = math.exp(
                                    c_para['lambda'] * epsilon_east)
                            if self.fodder_map[row + 1][col][0] == 'M' or \
                                    self.fodder_map[row + 1][col][0] == 'O':
                                propensity_south = 0
                            else:
                                if epsilon_south > 600:
                                    epsilon_south = 600
                                propensity_south = math.exp(
                                    c_para['lambda'] * epsilon_south)
                            if self.fodder_map[row][col - 1][0] == 'M' or \
                                    self.fodder_map[row][col - 1][0] == 'O':
                                propensity_west = 0
                            else:
                                if epsilon_west > 600:
                                    epsilon_west = 600
                                propensity_west = math.exp(
                                    c_para['lambda'] * epsilon_west)

                            propensity_tot = \
                                propensity_north + propensity_east + \
                                propensity_south + propensity_west

                            if propensity_tot == 0:
                                probability_north = 0
                                probability_east = 0
                                probability_south = 0
                                probability_west = 0
                            else:
                                probability_north = \
                                    propensity_north / propensity_tot
                                probability_east = \
                                    propensity_east / propensity_tot
                                probability_south = \
                                    propensity_south / propensity_tot
                                probability_west = \
                                    propensity_west / propensity_tot
                            probability_not_to_move = \
                                1 - probability_north - probability_east\
                                - probability_south - probability_west

                            choosen_cell = random.choices(
                                ['move_north', 'move_east', 'move_south',
                                 'move_west', 'not_move'],
                                weights=[probability_north, probability_east,
                                         probability_south, probability_west,
                                         probability_not_to_move])
                            if choosen_cell == ['move_north']:
                                self.migrated_carni[row - 1][col] += \
                                    self.carni_migration[row][col]
                            elif choosen_cell == ['move_east']:
                                self.migrated_carni[row][col + 1] += \
                                    self.carni_migration[row][col]
                            elif choosen_cell == ['move_south']:
                                self.migrated_carni[row + 1][col] += \
                                    self.carni_migration[row][col]
                            elif choosen_cell == ['move_west']:
                                self.migrated_carni[row][col - 1] += \
                                    self.carni_migration[row][col]
                            elif choosen_cell == ['stay']:
                                self.migrated_carni[row][col] += \
                                    self.carni_migration[row][col]

        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):
                if not self.migrated_carni[row][col]:
                    continue
                else:
                    self.island_map[row][col][1] += self.migrated_carni[row][col]

    def animal_in_cell_counter(self):

        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):

                if not self.island_map[row][col][0]:
                    continue
                else:
                    self.total_pop_herbi += len(self.island_map[row][col][0])
                if not self.island_map[row][col][1]:
                    continue
                else:
                    self.total_pop_carni += len(self.island_map[row][col][1])
        self.animal_dis = np.column_stack(
            (self.total_pop_herbi, self.total_pop_carni))

    def standard_map(self):
        island_string = self.island_string
        string_map = textwrap.dedent(island_string)
        string_map.replace('\n', ' ')

        color_code = {'O': colors.to_rgb('aqua'),
                      'M': colors.to_rgb('grey'),
                      'J': colors.to_rgb('forestgreen'),
                      'S': colors.to_rgb('yellowgreen'),
                      'D': colors.to_rgb('khaki')}

        island_map_vis = [[color_code[column] for column in row]
                          for row in string_map.splitlines()]

        self.ax_map.imshow(island_map_vis, interpolation='nearest')
        self.ax_map.set_xticks(range(len(island_map_vis[0])))
        self.ax_map.set_xticklabels(range(0, 1 + len(island_map_vis[0])))
        self.ax_map.set_yticks(range(len(island_map_vis)))
        self.ax_map.set_yticklabels(range(0, 1 + len(island_map_vis)))

        """for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                  'Savannah', 'Desert')):
            self.ax_map.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                             edgecolor='none',
                                             facecolor=color_code[name[0]]))
            self.ax_map.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

        """

        """
            map_colors = []
            for coord, cell in self.map.island.items():
                if cell.__name__ == 'Ocean':
                    map_colors.append(coord, map_colors['O'])
                elif cell.__name__ == 'Mountain':
                    map_colors.append([coord, map_colors['M'])
            [((0,2),  ]
            fig = plt.figure()
        """

    def _setup_graphics(self):
        """Creates subplots."""

        # create new figure window
        if self.fig is None:
            self.fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self.ax_map is None:
            self.ax_map = self.fig.add_subplot(221)
            self.standard_map()

        # Add right subplot for line graph of mean.
        if self.h_density is None:
            self.ax_heat_h = self.fig.add_subplot(223)
            self.heat_map_herbivore()

        if self.c_density is None:
            self.ax_heat_c = self.fig.add_subplot(224)
            self.heat_map_carnivore()

        if self.ax_line is None:
            self.ax_line = self.fig.add_subplot(322)
            if self.ymax_animals is not None:
                self.ax_line.set_ylim(0, self.ymax_animals)
            self.ax_line.set_xlim(0, self._final_year + 1)
            self.ax_line.set_title('Populations')

    def save_graphic(self):
        if self.img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self.img_ctr,
                                                     type=self.img_fmt))
        self.img_ctr += 1

    def update_population_plot(self):
        n_herb = self.total_count_herbi
        n_carn = self.total_count_carni
        self.y_label_h.append(n_herb)
        self.y_label_c.append(n_carn)
        self.ax_line.plot(range(self._year + 1), self.y_label_h,
                          'g', self.y_label_c, 'r')
        self.ax_line.legend(['Herbivore', 'Carnivore'])

    def heat_map_herbivore(self):
        """
        A method that shows the population in each cell by showing colors
        :return:
        """

        herb_cell = self.animal_distribution.pivot('Row', 'Col', 'Herbivore')

        self.h_density = self.ax_heat_h.imshow(herb_cell,
                                               interpolation='nearest',
                                               cmap='Greens')
        self.ax_heat_h.set_title('Herbivore population density')

    def heat_map_carnivore(self):

        carn_cell = self.animal_distribution.pivot('Row', 'Col', 'Carnivore')

        self.c_density = self.ax_heat_c.imshow(carn_cell,
                                               interpolation='nearest',
                                               cmap='Reds')
        self.ax_heat_c.set_title('Carnivore population density')

    def update_all(self):
        self.heat_map_herbivore()
        self.heat_map_carnivore()
        self.update_population_plot()
        plt.pause(1e-6)

    def simulate(self, num_years, vis_years=1, img_years=1):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        if img_years is None:
            img_years = vis_years

        self._final_year = self._year + num_years
        self._setup_graphics()

        while self._year < self._final_year:
            if self._year % vis_years == 0:
                self.update_all()
            if self._year % img_years == 0:
                self.save_graphic()

            self.simulation_one_year()
            self.migrate_herbivores()
            self.migrate_carnivores()
            self._year += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        new_herbi, new_carni, position = self.landscape.set_pop(population)
        for i in range(len(self.island_map)):
            for j in range(len(self.island_map[0])):
                if (i, j) == position:
                    self.island_map[i][j][0] += new_herbi
                    self.island_map[i][j][1] += new_carni

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.total_count_herbi + self.total_count_carni

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):
                self.total_count_herbi += len(self.island_map[row][col][0])
                self.total_count_carni += len(self.island_map[row][col][1])
        dic_animal_per_species = {'Herbivore': self.total_count_herbi,
                                  'Carnivore': self.total_count_carni}
        return dic_animal_per_species

    @property
    def animal_distribution(self):
        """
        Pandas DataFrame with animal count per species for each cell on island.
        """
        data = {}
        rows = []
        cols = []
        herbi = []
        carni = []
        for row in range(len(self.island_map)):
            for col in range(len(self.island_map[0])):
                herbi.append(len(self.island_map[row][col][0]))
                carni.append(len(self.island_map[row][col][1]))
                rows.append(row)
                cols.append(col)
        data['Row'] = rows
        data['Col'] = cols
        data['Herbivore'] = herbi
        data['Carnivore'] = carni
        df = pd.DataFrame(data)
        df = df[['Row', 'Col', 'Herbivore', 'Carnivore']]
        return df

    def make_movie(self):
        """
        Create MPEG4 movie from visualization images saved.
        """
        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/
                # Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)
    """

    def heat_map(self):
       
               Returns a heat-map, describing population density and movements
       

        self.herbi_per_cell = np.asarray(self.total_pop_herbi)
        self.ax_heat_h = sns.heatmap(self.herbi_per_cell,
                                     interpolation='nearest',
                                     cmap='Greens')
        self.ax_heat_h.set_title('Herbivore density')

        self.carni_per_cell = np.asarray(self.total_pop_carni)
        self.ax_heat_c = sns.heatmap(self.carni_per_cell,
                                     interpolation='nearest',
                                     cmap='Reds')
        self.ax_heat_c.set_title('Carnivore density')
        plot.show()()

    """

if __name__ == "__main__":
    Geo = """\
                 OOOOOOO
                 OJSSDDO
                 OJSDDOO
                 OOOOOOO"""

    ini_herbs = [{'loc': (1, 1),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 10}
                          for _ in range(5)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 60}
                          for _ in range(5)]}]
    sim = BioSim(Geo, ini_herbs, seed=123456)
    sim.simulate(20)

        # print(sim.num_animals_per_species)
    #sim.plot_island_population()
    sim.heat_map_herbivore()
    sim.heat_map_carnivore()
    sim.heat_map_carnivore()
    sim.setup_graphics()
    sim.standard_map()
