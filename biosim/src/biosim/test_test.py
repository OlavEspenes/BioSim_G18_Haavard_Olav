from landscape import Landscape
from cell import Cell

if __name__ == "__main__":

    olafius = Landscape("""\
    OOO
    OJO
    OOO""")
    olafius.array_map()
    kart = olafius.assign_tile()
    print(kart)
    print(kart[4].fodder)
    print()

if __name__ == "__main__":

    proc = Cell()



