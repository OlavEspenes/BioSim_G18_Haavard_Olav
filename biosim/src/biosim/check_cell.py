
from cell import Cell

if __name__ == "__main__":
    h_parameters = {'w_birth': 8.0,
                  'sigma_birth': 4.0,
                  'beta': 0.9,
                  'eta': 0.05,
                  'a_half': 40.0,
                  'phi_age': 0.2,
                  'w_half': 10.0,
                  'phi_weight': 0.1,
                  'mu': 0.25,
                  'lambda': 1.0,
                  'gamma': 0.2,
                  'zeta': 3.5,
                  'xi': 1.2,
                  'omega': 0.4,
                  'F': 10.0}
    c_parameters = {'w_birth': 6.0,
                                'sigma_birth': 1.0,
                                'beta': 0.75,
                                'eta': 0.125,
                                'a_half': 60.0,
                                'phi_age': 0.4,
                                'w_half': 4.0,
                                'phi_weight': 0.4,
                                'mu': 0.4,
                                'lambda': 1.0,
                                'gamma': 0.8,
                                'zeta': 3.5,
                                'xi': 1.1,
                                'omega': 0.9,
                                'F': 50.0,
                                'DeltaPhiMax': 10.0}
    ini_pop = [{'loc': (1, 1)},
               {'pop': [{'species': 'Herbivore',
                         'age': 3,
                         'weight': 20}, {'species': 'Herbivore',
                                         'age': 3,
                                         'weight': 20},
                        {'species': 'Carnivore',
                         'age': 3,
                         'weight': 20}, {'species': 'Herbivore',
                                         'age': 3,
                                         'weight': 20},
                        {'species': 'Herbivore',
                         'age': 3,
                         'weight': 20}, {'species': 'Carnivore',
                                         'age': 3,
                                         'weight': 20}, ]}]
    carni = []
    herbi = []
    for i in ini_pop[1].get('pop'):
        if i.get('species') == 'Herbivore':
            herbi.append(i)
        elif i.get('species') == 'Carnivore':
            carni.append(i)
    position = (1,1)
    fodder = 1000
    test = Cell(herbi, carni, fodder, h_parameters, c_parameters, position)
    #test.age()
    #test.feeding_herbi()
    #test.feeding_carni()
    #test.birth()
    #test.weight_loss()
    test.where_to_migrate()
    #test.death()

    print(carni)
    print(herbi)



