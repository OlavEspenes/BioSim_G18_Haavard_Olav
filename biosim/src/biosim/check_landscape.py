from biosim.simulation import BioSim
from biosim.landscape import Landscape
if __name__ == "__main__":
    ini_pop = [{'loc': (0, 0)},
               {'pop': [{'species': 'Herbivore',
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
                         'weight': 80}
                        ]}]
    island_map = """
        O
        """
    land = Landscape(island_map)
    sim = BioSim(island_map,
        [],
        12345,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png")

    #sim.simulation_one_year()
    sim.simulate(7)

