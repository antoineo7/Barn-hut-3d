from Controller import *

SIZE_X = 1300
SIZE_Y = 600
SIZE_Z = 600
MASSE_MIN = 1000
MASSE_MAX = 10000
TAILLE_MIN = 3
TAILLE_MAX = 7
THETA = 0.9
G = 0.1
VITESSE_MIN = 0.00
VITESSE_MAX = 0.0
dt = 0.003
NBR_PLANETES = 2000
EPSILON = 2

engine = Engine(SIZE_X, SIZE_Y, SIZE_Z,
                MASSE_MIN, MASSE_MAX, TAILLE_MIN, TAILLE_MAX,
                THETA, G, VITESSE_MIN, VITESSE_MAX, dt, NBR_PLANETES, EPSILON)
view = View(engine, from_file=True, file_name='circle2kvit.txt')
app = Controller(engine, view)
app.run()

