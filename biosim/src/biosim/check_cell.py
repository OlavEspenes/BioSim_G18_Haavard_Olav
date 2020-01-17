
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
    carni = []
    herbi = []
    for i in ini_pop[1].get('pop'):
        if i.get('species') == 'Herbivore':
            herbi.append(i)
        elif i.get('species') == 'Carnivore':
            carni.append(i)
    position = (1,1)
    fodder = 1000
    test = Cell(herbi, carni, fodder, h_parameters, c_parameters)
    test.feeding_herbi()
    test.feeding_carni()
    test.birth()
    test.age()
    test.weight_loss()
    test.death()
    flykninger = test.send_out_emigrators()         #gives us emigrants. two lists for each species
    print('herbi som skal flytte',flykninger[0])    #herbi
    print('carni som skal flytte',flykninger[1])    #carni
    print('herbi igjen i cellen', herbi)
    print('carni igjen i cellen', carni)





