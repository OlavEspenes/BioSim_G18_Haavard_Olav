from biosim.simulation import BioSim
from biosim.landscape import Landscape
if __name__ == "__main__":
    ini_pop = [{'loc': (2, 2)},
               {'pop': [{'species': 'Herbivore',
                         'age': 2,
                         'weight': 10}, {'species': 'Herbivore',
                                         'age': 3,
                                         'weight': 20},
                         {'species': 'Herbivore',
                                         'age': 4,
                                         'weight': 15},
                        {'species': 'Herbivore',
                         'age': 5,
                         'weight': 200},
                        ]}]
    island_map = """
        OOOOO
        OJJJO
        OJJJO
        OJJJO
        OOOOO
        """
    land = Landscape(island_map)
    sim = BioSim(island_map,
        ini_pop,
        53793,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png")

    #sim.simulation_one_year()
    sim.simulate(10)
