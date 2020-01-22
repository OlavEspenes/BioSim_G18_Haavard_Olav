# Project Rossumøya
#### Coders 
- Håvard Brobakken Eig (harvardei@nmbu.no)
- Olav Vikøren Espenes (olaves@nmbu.no) 

#### Introduction
Project "Modelling the Ecosystem of Rossumøya" were given as a task to solve in 
in the subject INF200 at Norwegian School of Life Sciences, NMBU in januar 2020. The project simulates how the ecosystem at Rossumøya develops through a set amount of years at a given island.
Head of the ecosystem simulation, the Biosim class, runs a simulation of the island ecosystem consisting of herbivores and carnivores distributed across different geographical areas. The simulation runs a given number of years based on a given number of animals inserted at year zero, and their associated parameters. Animals can migrate, feed and die based on fitness and probability calculation. This, together with several other requirements, makes the simulation a credible representation of a possible ecosystem. 

#### Cell
The Cell class contains methods that allow an annual 
cycle to be performed for a given position on the map 
based on the animals belonging to the cell and available fodder. 
An annual cycle consists of feeding, procreation, migration, aging, loss of weight and death.
Cell takes inputs in herbivore fodder determined by geographical type. This sets much of the criterion for further development in the cell.

### Landscape
Landscape controls parameters and makes it possible to set their own parameters. 
This applies to parameters for herbivores and carnivores, 
as well as the types of jungle and savannah. 
Landscape contains methods for generating new fodder, determining the island map and placing population. 

### Biosim
Running simulation for one year as well as a desired number of years. Creates associated 
visualization for these simulations. Also consists of migration method and moviemaker.