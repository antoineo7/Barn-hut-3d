from Controller import *


def write_to_file(file_name,nbr_iter,engine,verbose=False):

    f = open(file_name,"w")
    for k in range(nbr_iter):
        engine.timestep()
        s = engine.get_coords()
        string = ""
        for tuple in s:
            string+=str(tuple)[1:-1]+";"
        f.write(string+"\n")
        if verbose:
            print k/float(nbr_iter)

    f.close()

if __name__ == '__main__':
    SIZE_X = 1300
    SIZE_Y = 600
    SIZE_Z = 600
    MASSE_MIN = 1000
    MASSE_MAX = 10000
    TAILLE_MIN = 3
    TAILLE_MAX = 7
    THETA = 0.9
    G = 0.1
    VITESSE_MIN = 100.00
    VITESSE_MAX = 200.00
    dt = 0.003
    NBR_PLANETES = 2000
    EPSILON = 2

    engine = Engine(SIZE_X, SIZE_Y, SIZE_Z,
                    MASSE_MIN, MASSE_MAX, TAILLE_MIN, TAILLE_MAX,
                    THETA, G, VITESSE_MIN, VITESSE_MAX, dt, NBR_PLANETES, EPSILON)

    write_to_file("circle2kvit.txt",100,engine,verbose=True)
