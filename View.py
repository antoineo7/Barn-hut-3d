from direct.showbase.ShowBase import ShowBase
from Engine import *
from direct.task import Task
from panda3d.core import NodePath, TextNode
from direct.gui.DirectGui import *
from random import *


class View(ShowBase):

    def __init__(self, engine):
        ShowBase.__init__(self)

        self.engine = engine

        self.camera.setPos(SIZE_X / 2.0, SIZE_Y / 2.0, 0)
        self.camera.setHpr(0, 90, 0)
        self.disableMouse()
        self.setBackgroundColor(0, 0, 0)
        self.textures = [self.loader.loadTexture("models/"+str(k)+".jpg") for k in range(1,9)]
        self.bodies = []
        self.ini_planets()
        self.taskMgr.add(self.animate_planet, "AnimatePlanet")

    def ini_planets(self):
        for x, y, z in self.engine.get_coords():
            self.bodies.append(self.loader.loadModel("models/planet_sphere"))
            self.bodies[-1].setTexture(self.textures[randint(0,7)], 1)
            self.bodies[-1].reparentTo(self.render)
            self.bodies[-1].setScale(1, 1, 1)
            self.bodies[-1].setPos(x, y, z)

    def animate_planet(self, task):
        self.engine.timestep()
        for (x, y, z), body in zip(self.engine.get_coords(), self.bodies):
            body.setPos(x, y, z)
        return Task.cont


SIZE_X = 1300
SIZE_Y = 600
SIZE_Z = 600
MASSE_MIN = 1000
MASSE_MAX = 10000
TAILLE_MIN = 3
TAILLE_MAX = 7
THETA = 0.8
G = 0.1
VITESSE_MIN = 0.00
VITESSE_MAX = 0.0
dt = 0.01
NBR_PLANETES = 10
EPSILON = 2
engine = Engine(SIZE_X, SIZE_Y, SIZE_Z,
                MASSE_MIN, MASSE_MAX, TAILLE_MIN, TAILLE_MAX,
                THETA, G, VITESSE_MIN, VITESSE_MAX, dt, NBR_PLANETES, EPSILON)
app = View(engine)
app.run()
