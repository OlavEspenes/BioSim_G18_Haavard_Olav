from landscape import Landscape

if __name__ == "__main__":

    olafius = Landscape("""\
    OOO
    OJO
    OOO""")
    olafius.map_list()
    kart = olafius.assign_tile()
    print(kart)
    print(kart[4].fodder)
    print(kart[4].coordinates)
    print()
