from landscape import Landscape
if __name__ == "__main__":

    test = Landscape("""\
    OOO
    OJO
    OOO""")
    test.string_to_matrix()
    print(test.assign_tile())
    test.c_parameters('mu')