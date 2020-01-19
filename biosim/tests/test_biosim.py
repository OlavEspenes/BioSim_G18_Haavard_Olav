# -*- coding: utf-8 -*-

"""

"""

__author__ = "Olav Vikøren Espenes & Håvard Brobakken Eig"
__email__ = "olaves@nmbu.no, havardei@nmbu.no"

from cell import Cell
from simulation import BioSim

class TestBiosim:
    @pytest.fixture()
    def create_variables(self):

