from simulation import BioSim

if __name__ == "__main__":
    ini_pop = [{'loc': (1, 1)},
               {'pop': [{'species': 'Herbivore',
                         'age': 2,
                         'weight': 10}, {'species': 'Herbivore',
                                         'age': 3,
                                         'weight': 20},
                        {'species': 'Carnivore',
                         'age': 3,
                         'weight': 40}, {'species': 'Herbivore',
                                         'age': 4,
                                         'weight': 15},
                        {'species': 'Herbivore',
                         'age': 5,
                         'weight': 20}, {'species': 'Carnivore',
                                         'age': 3,
                                         'weight': 20}, ]}]
    ini_island = """
    J
    """
    test = BioSim(ini_pop, ini_island, 123)