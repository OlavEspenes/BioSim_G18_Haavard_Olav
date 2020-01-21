# -*- coding: utf-8 -*-

"""
"""

__author__ = ""
__email__ = ""

import math
from biosim.cell import Cell
from biosim.landscape import Landscape
import random
import pandas as pd
import seaborn as sns; sns.set()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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
        ini_carni = []
        ini_herbi = []
        self.ini_position = (0, 0)
        if ini_pop:
            for i in ini_pop[1].get('pop'):
                if i.get('species') == 'Herbivore':
                    ini_herbi.append(i)
                elif i.get('species') == 'Carnivore':
                    ini_carni.append(i)
            self.ini_position = ini_pop[0].get('loc')

        self.landscape = Landscape(island_map)
        self.fodder_map = self.landscape.make_fodder_island(island_map)
        self.island_map = self.landscape.make_island_map(self.fodder_map,
                                                         self.ini_position,
                                                         ini_herbi, ini_carni)

        self.year_count = 0
        rows = len(self.island_map)
        columns = len(self.island_map[0])
        df_labels = ['x', 'y', 'Herbivores', 'Carnivores']
        empty_df = [[i + 1, j + 1, 0, 0] for j in range(columns)
                    for i in range(rows)]
        self.pop_by_cell = pd.DataFrame(data=empty_df, columns=df_labels)
        self.pop_by_cell.update(ini_pop)
        self.graph_label = None
        self.ax_herb = None
        self.ax_carn = None
        self.map_label = None


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
            self.landscape.set_parameters_herbi(params)
        elif species == 'Carnivores':
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
        herbi_migration = [[[] for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))]
        carni_migration = [[[] for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))]
        migrated_herbi = [[[] for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))]
        migrated_carni = [[[] for i in range(len(self.fodder_map[1]))] for j in range(len(self.fodder_map))]
        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):
                if self.island_map[row][col][0] is not None or \
                        self.island_map[row][col][1] is not None:
                    herbi = self.island_map[row][col][0]
                    carni = self.island_map[row][col][1]
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
                    #food = cell.feeding_herbi()
                    #cell.feeding_carni()
                    #cell.birth()
                    #cell.age()
                    #cell.weight_loss()
                    #cell.death()
                    #emigrations = cell.send_out_emigrators()
                    herbi_migration[row][col] = emigrators[0]
                    carni_migration[row][col] = emigrators[1]
                    self.fodder_map[row][col][1] = food

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
                            if not self.island_map[row-1][col][0]:
                                epsilon_north = north_f/(1*h_para['F'])
                            else:
                                epsilon_north = north_f/(len(self.island_map[row-1][col][0])+1)*h_para['F']
                            if not self.island_map[row][col+1][0]:
                                epsilon_east = east_f/(1*h_para['F'])
                            else:
                                epsilon_east = east_f/(len(self.island_map[row][col+1][0])+1)*h_para['F']
                            if not self.island_map[row+1][col][0]:
                                epsilon_south = south_f / (1*h_para['F'])
                            else:
                                epsilon_south = south_f/(len(self.island_map[row+1][col][0])+1)*h_para['F']
                            if not self.island_map[row][col-1][0]:
                                epsilon_west = west_f / (1*h_para['F'])
                            else:
                                epsilon_west = west_f/(len(self.island_map[row][col-1][0])+1)*h_para['F']

                            if self.fodder_map[row-1][col][0] == 'M' or \
                                    self.fodder_map[row-1][col][0] == 'O':
                                propensity_north = 0
                            else:
                                if epsilon_north > 600:
                                    epsilon_north = 600
                                propensity_north = math.exp(h_para['lambda']*epsilon_north)
                            if self.fodder_map[row][col+1][0] == 'M' or \
                                    self.fodder_map[row][col+1][0] == 'O':
                                propensity_east = 0
                            else:
                                if epsilon_east > 600:
                                    epsilon_east = 600
                                propensity_east = math.exp(h_para['lambda']*epsilon_east)
                            if self.fodder_map[row+1][col][0] == 'M' or \
                                    self.fodder_map[row+1][col][0] == 'O':
                                propensity_south = 0
                            else:
                                if epsilon_south > 600:
                                    epsilon_south = 600
                                propensity_south = math.exp(h_para['lambda']*epsilon_south)
                            if self.fodder_map[row][col-1][0] == 'M' or \
                                    self.fodder_map[row][col-1][0] == 'O':
                                propensity_west = 0
                            else:
                                if epsilon_west > 600:
                                    epsilon_west = 600
                                propensity_west = math.exp(h_para['lambda']*epsilon_west)

                            propensity_tot = propensity_north+propensity_east+propensity_south+propensity_west
                            if propensity_tot == 0:
                                probability_north = 0
                                probability_east = 0
                                probability_south = 0
                                probability_west = 0
                            else:
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

        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):
                if not migrated_herbi[row][col]:
                    continue
                else:
                    self.island_map[row][col][0] += migrated_herbi[row][col]

        if not carni_migration:
            pass
        else:
            for row, _ in enumerate(carni_migration):
                for col, _ in enumerate(carni_migration[0]):
                    if carni_migration[row][col] is None:
                        continue
                    else:
                        for c_migrant, _ in enumerate(carni_migration[row][col]):
                            north_f = 0
                            east_f = 0
                            south_f = 0
                            west_f = 0
                            for h in range(len(self.island_map[row-1][col][0])):
                                north_f += self.island_map[row-1][col][0][h]['weight']
                            for h in range(len(self.island_map[row][col+1][0])):
                                east_f += self.island_map[row][col+1][0][h]['weight']
                            for h in range(len(self.island_map[row+1][col][0])):
                                south_f += self.island_map[row+1][col][0][h]['weight']
                            for h in range(len(self.island_map[row][col-1][0])):
                                west_f += self.island_map[row][col-1][0][h]['weight']

                            epsilon_north = north_f/(len(self.island_map[row-1][col][1])+1)*c_para['F']
                            epsilon_east = east_f/(len(self.island_map[row][col+1][1])+1)*c_para['F']
                            epsilon_south = south_f/(len(self.island_map[row+1][col][1])+1)*c_para['F']
                            epsilon_west = west_f/(len(self.island_map[row][col-1][1])+1)*c_para['F']

                            if self.fodder_map[row-1][col][0] == 'M' or \
                                    self.fodder_map[row-1][col][0] == 'O':
                                propensity_north = 0
                            else:
                                if epsilon_north > 600:
                                    epsilon_north = 600
                                propensity_north = math.exp(c_para['lambda']*epsilon_north)
                            if self.fodder_map[row][col+1][0] == 'M' or \
                                    self.fodder_map[row][col+1][0] == 'O':
                                propensity_east = 0
                            else:
                                if epsilon_east > 600:
                                    epsilon_east = 600
                                propensity_east = math.exp(c_para['lambda']*epsilon_east)
                            if self.fodder_map[row+1][col][0] == 'M' or \
                                    self.fodder_map[row+1][col][0] == 'O':
                                propensity_south = 0
                            else:
                                if epsilon_south > 600:
                                    epsilon_south = 600
                                propensity_south = math.exp(c_para['lambda']*epsilon_south)
                            if self.fodder_map[row][col-1][0] == 'M' or \
                                    self.fodder_map[row][col-1][0] == 'O':
                                propensity_west = 0
                            else:
                                if epsilon_west > 600:
                                    epsilon_west = 600
                                propensity_west = math.exp(c_para['lambda']*epsilon_west)

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
                                                          weights=[
                                                            probability_north,
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

        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):
                if not migrated_carni[row][col]:
                    continue
                else:
                    self.island_map[row][col][1] += migrated_carni[row][col]



    def animal_in_cell_counter(self):
        self.total_pop_herbi = [[[] for i in range(len(self.island_map))] for j in
                           range(len(self.island_map))]
        self.total_pop_carni = [[[] for i in range(len(self.island_map))] for j in
                           range(len(self.island_map))]
        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):

                if not self.island_map[row][col][0]:
                    continue
                else:
                    self.total_pop_herbi[row][col] = len(self.island_map[row][col][0])
                if not self.island_map[row][col][1]:
                    continue
                else:
                    self.total_pop_carni[row][col] = len(self.island_map[row][col][1])
        self.animal_dis = np.column_stack((self.total_pop_herbi, self.total_pop_carni))

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """

        self.new_sim = True
        for i in range(num_years):
            self.simulation_one_year()
            self.animal_in_cell_counter()

            if self.year_count % vis_years == 0:
                plt.ion()

            self.year_count += 1
            if self.year_count % img_years == 0:
                plt.savefig('biosim/animation/biosim_' +
                            str(self.year_count).zfill(5) + '.png')

        print(self.island_map)
        print(self.fodder_map)
        print(self.animal_in_cell_counter)


    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        pass


    @property
    def year(self):
        """Last year simulated."""
        print('Last year simulated: ', self.year_count)
        return self.year_count

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.total_count_herbi + self.total_count_carni


    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

        self.total_count_herbi = 0
        self.total_count_carni = 0
        for row, _ in enumerate(self.island_map):
            for col, _ in enumerate(self.island_map[0]):
                self.total_count_herbi += len(self.island_map[row][col][0])
                self.total_sount_carni += len(self.island_map[row][col][1])
        return(self.total_count_herbi)
        return(self.total_count_carni)



    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

        population = pd.DataFrame(self.animal_in_cell_counter(), columns=['Herbivores', 'Carnivores'])
        self.pop_by_cell.update(ini_pop)
        return self.pop_by_cell

    def replot(n_steps):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim(0, n_steps)
        ax.set_ylim(0, 1)

        data = []
        for _ in range(n_steps):
            data.append(np.random.random())
            ax.plot(data, 'b-')
            plt.pause(1e-6)

    def update(n_steps):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim(0, n_steps)
        ax.set_ylim(0, 1)

        line = ax.plot(np.arange(n_steps),
                       np.full(n_steps, np.nan), 'b-')[0]

        for n in range(n_steps):
            ydata = line.get_ydata()
            ydata[n] = np.random.random()
            line.set_ydata(ydata)
            plt.pause(1e-6)

    def heat_map(self):
        """
        Returns a heat-map, describing population density and movements
        """

        self.herbi_per_cell = np.asarray(self.total_pop_herbi)
        self.ax_herb = sns.heatmap(self.herbi_per_cell, vmin = 0, vmax = 200)
        self.ax_herb.set_title('Herbivore density')

        self.carni_per_cell = np.asarray(self.total_pop_carni)
        self.ax_herb = sns.heatmap(self.carni_per_cell)
        self.ax_carn.set_title('Carnivore density')

    def plot_map(self):
        """
        Yngve plot: https://github.com/yngvem/INF200-2019/blob/master/lectures/J05/Plotting/mapping.py

        """
        #                   R    G    B
        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                    for row in map.splitlines()]

        fig = plt.figure()

        axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        axim.imshow(map_rgb)
        axim.set_xticks(range(len(map_rgb[0])))
        axim.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        axim.set_yticks(range(len(map_rgb)))
        axim.set_yticklabels(range(1, 1 + len(map_rgb)))

        axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                   'Savannah', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

        plt.show()


    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

