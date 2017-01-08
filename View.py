from direct.showbase.ShowBase import ShowBase
from Engine import *
from direct.task import Task
from panda3d.core import NodePath, TextNode
from direct.gui.DirectGui import *
from random import *
import sys


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

        # Keys handler initialization :
        # Space bar allows to control the camera rotation, whereas the arrow keys control the x,z translation

        self.keys = {"turnLeft": 0, "turnRight": 0,
                     "up": 0, "down": 0, "hold": 0}

        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["turnLeft", 1])
        self.accept("arrow_left-up", self.setKey, ["turnLeft", 0])
        self.accept("arrow_right", self.setKey, ["turnRight", 1])
        self.accept("arrow_right-up", self.setKey, ["turnRight", 0])
        self.accept("arrow_up", self.setKey, ["up", 1])
        self.accept("arrow_up-up", self.setKey, ["up", 0])
        self.accept("arrow_down", self.setKey, ["down", 1])
        self.accept("arrow_down-up", self.setKey, ["down", 0])
        self.accept("r", self.reset_camera)

        self.accept("space", self.setKey, ["hold", 1])
        self.accept("space-up", self.setKey, ["hold", 0])

        self.arrow_left_text = OnscreenText(text="[Arrow Left/Right] : x control", pos=(0.95, -0.95),
                                            scale=0.04, fg=(255, 255, 255, 1), align=TextNode.ACenter, mayChange=1)
        self.arrow_up_text = OnscreenText(text="[Arrow Up/down] : z control", pos=(0.95, -0.90),
                                          scale=0.04, fg=(255, 255, 255, 1), align=TextNode.ACenter, mayChange=1)
        self.arrow_space_text = OnscreenText(text="[Space] : Switch to angle Control", pos=(0.95, -0.85),
                                            scale=0.04, fg=(255, 255, 255, 1), align=TextNode.ACenter, mayChange=1)
        self.arrow_esc_text = OnscreenText(text="[Escape] : Quit", pos=(0.95, -0.80),
                                             scale=0.04, fg=(255, 255, 255, 1), align=TextNode.ACenter, mayChange=1)

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

        newPosx, newPosy, newPosz = self.camera.getPos()
        newAnglex, newAngley, newAnglez = self.camera.getHpr()

        newPosx += self.keys['turnLeft']
        newPosx -= self.keys['turnRight']
        newPosz += self.keys['up']
        newPosz -= self.keys['down']

        newAngley += (self.keys['hold'] == 1) * self.keys['up']
        newAngley -= (self.keys['hold'] == 1) * self.keys['down']

        newAnglex += (self.keys['hold'] == 1) * self.keys['turnLeft']
        newAnglex -= (self.keys['hold'] == 1) * self.keys['turnRight']

        self.camera.setPos(newPosx, newPosy, newPosz)
        self.camera.setHpr(newAnglex, newAngley, newAnglez)
        return Task.cont

    def setKey(self, key, val):
        self.keys[key] = val

    def reset_camera(self):
        self.camera.setPos(SIZE_X / 2.0, SIZE_Y / 2.0, 0)
        self.camera.setHpr(0, 90, 0)


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
