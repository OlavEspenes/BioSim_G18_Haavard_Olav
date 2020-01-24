from biosim.simulation import BioSim
from biosim.landscape import Landscape
if __name__ == "__main__":
    ini_pop = [{'loc': (1, 1),
               'pop': [{'species': 'Herbivore',
                        'age': 5,
                        'weight': 20},
                       {'species': 'Herbivore',
                        'age': 5,
                        'weight': 20},
                       {'species': 'Herbivore',
                        'age': 5,
                        'weight': 20},
                       {'species': 'Herbivore',
                        'age': 5,
                        'weight': 20},
                       {'species': 'Herbivore',
                        'age': 20,
                        'weight': 80},
                       {'species': 'Herbivore',
                        'age': 20,
                        'weight': 80}]}]
    island_map = """\
               OOOOO
               OJJJO
               OJJJO
               OOOOO"""
    land = Landscape(island_map)
    sim = BioSim(island_map,
                 ini_pop,
                 123456,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=None,
                 img_fmt="png")

    # sim.simulation_one_year()
    # sim._setup_graphics()
    sim.simulate(10)
    print(sim.animal_distribution)
    print(sim.fodder_map)
    print(sim.island_map)
