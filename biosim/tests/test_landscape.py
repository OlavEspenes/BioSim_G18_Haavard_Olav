# -*- coding: utf-8 -*-

"""

"""

__author__ = "Olav Vikøren Espenes & Håvard Brobakken Eig"
__email__ = "olaves@nmbu.no, havardei@nmbu.no"

from biosim.landscape import Landscape
import pytest
import random


class TestLandscape:
    @pytest.fixture()
    def create_island(self):
        self.island = """OOO
                        OJO
                        OOO"""
        self.landscape = Landscape(self.island)

    def test_make_fodder_island(self):
        pass

    def test_make_island_map(self):
        pass
