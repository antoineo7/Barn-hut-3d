
from utils import *

def write_to_file(file_name,nbr_iter,engine,verbose=False):

    f = open(file_name, "w")
    for k in range(nbr_iter):
        engine.timestep()
        s = engine.get_coords()
        string = ""
        for tuple in s:
            string += str(tuple)[1:-1]+";"
        f.write(string+"\n")
        if verbose:
            print k/float(nbr_iter)

    f.close()

if __name__ == '__main__':
    from Engine import *
    engine = Engine(read_params("Nuit1"))
    write_to_file("simulation/Nuit1.txt", 10000, engine, verbose=True)
