
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import *
from direct.task import Task
from panda3d.core import *
from direct.gui.DirectGui import *
from random import *
import sys
import math
from panda3d.core import loadPrcFileData


class View(ShowBase):

    def __init__(self, controller, from_file=False, file_name=None):
        #loadPrcFileData('', 'fullscreen true')
        ShowBase.__init__(self)
        self.controller = controller
        self.SIZE_X, self.SIZE_Y, self.SIZE_Z = self.controller.get_engine_size()
        self.camera.setPos(self.SIZE_X / 2.0, self.SIZE_Y / 2.0, 250)
        self.camera.setHpr(0, 90, 0)
        self.disableMouse()
        self.setBackgroundColor(0, 0, 0)
        self.light = AmbientLight('alight')
        self.light.setColor(VBase4(0.2,0.2,0.2,1))
        self.render.setLight(self.render.attachNewNode(self.light))

        self.directionalLight = DirectionalLight('directionalLight')
        self.directionalLight.setColor(Vec4(0.8, 0.8, 0.8, 1))
        self.directionalLightNP = self.render.attachNewNode(self.directionalLight)
        # This light is facing backwards, towards the camera.
        self.directionalLightNP.setHpr(500, 200, 200)
        self.render.setLight(self.directionalLightNP)
        if not from_file:
            self.thetaParam = DirectSlider(range=(0, 1), value=self.controller.get_theta_parameter(), pageSize=3,
                                       command=self.setValue, pos=(0.95,0,0.9))
            self.thetaParam.set_scale(0.2)
            self.label = OnscreenText(text="Theta parameter", pos=(0.95, 0.95),
                     scale=0.04, fg=(255, 255, 255, 1), align=TextNode.ACenter, mayChange=1)




        self.bodies = []
        self.taskMgr.add(self.animate_planet, "AnimatePlanet")
        self.from_file = from_file
        if file_name is None:
            self.file = None
        else:
            self.file = open(file_name, 'r')
        self.ini_planets()

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
        if not self.from_file:
            for x, y, z in self.controller.get_coords():
                self.bodies.append(self.loader.loadModel("models/planet_sphere"))
                self.bodies[-1].reparentTo(self.render)
                self.bodies[-1].setScale(0.05)
                self.bodies[-1].setPos(x, y, z)
        else:
            tmp2 = self.file.readline().split(";")[:-1]
            if len(tmp2)!=self.controller.get_planets_number():
                print("N-Bodies from engine parameters and file don't match ")
            for str_tuple in tmp2:
                tmp = str_tuple.split(",")
                x, y, z = float(tmp[0]), float(tmp[1]), float(tmp[2])
                self.bodies.append(self.loader.loadModel("models/planet_sphere"))
                self.bodies[-1].reparentTo(self.render)
                self.bodies[-1].setScale(0.03)
                self.bodies[-1].setPos(x, y, z)

    def animate_planet(self, task):
        if not self.from_file:
            self.controller.update_pos()
            for (x, y, z), body in zip(self.controller.get_coords(), self.bodies):
                body.setPos(x, y, z)
        else:
            for str_tuple, body in zip(self.file.readline().split(";")[:-1],self.bodies):
                tmp = str_tuple.split(",")
                x, y, z = float(tmp[0]), float(tmp[1]), float(tmp[2])
                body.setPos(x, y, z)


        newPosx, newPosy, newPosz = self.camera.getPos()
        newAnglexint, newAngleyint, newAnglezint = self.camera.getHpr()
        newAnglex,newAngley,newAnglez = float(newAnglexint),float(newAngleyint),float(newAnglezint)
        norm = float(math.sqrt(newAnglex**2+newAngley**2+newAnglez**2))
        dx,dy,dz = newAnglex/norm,newAngley/norm,newAnglez/norm

        if self.keys['up'] and not self.keys['hold']:
            newPosx+=dz
            newPosy+=dx
            newPosz+=dy
        if self.keys['down'] and not self.keys['hold']:
            newPosx -= dz
            newPosy -= dx
            newPosz -= dy



        newPosx -= self.keys['turnLeft']
        newPosx += self.keys['turnRight']

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
        self.camera.setPos(self.SIZE_X / 2.0, self.SIZE_Y / 2.0, 0)
        self.camera.setHpr(0, 90, 0)

    def setValue(self):
        self.controller.set_theta_value(self.thetaParam['value'])




if __name__ == "__main__":
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
    NBR_PLANETES = 5
    EPSILON = 2
    engine = Engine(SIZE_X, SIZE_Y, SIZE_Z,
                    MASSE_MIN, MASSE_MAX, TAILLE_MIN, TAILLE_MAX,
                    THETA, G, VITESSE_MIN, VITESSE_MAX, dt, NBR_PLANETES, EPSILON)
    app = View(engine)
    app.run()


class View2(ShowBase):
    def __init__(self, controller):
        ShowBase.__init__(self)
        self.controller = controller

        OnscreenText(text="Welcome to Galaxy Simulator", pos=(0, 0.70),
                     scale=0.18, fg=(255, 255, 255, 1), align=TextNode.ACenter, mayChange=1)
        OnscreenText(text="By Antoine Mahe and Frederic Wantiez", pos=(0.9, -0.85),
                     scale=0.04, fg=(255, 255, 255, 1), align=TextNode.ACenter, mayChange=1)
        b1 = DirectButton(text="Live Mode", scale=.1, command=self.launch_live, pos=(-0.4,0,0.1))
        b2 = DirectButton(text="PreCalc Mode", scale=.1, command=self.launch_live, pos=(0.4,0,0.1))
        b = OnscreenImage(parent=render2d, image="models/bg.jpg")

    def launch_live(self):
        self.controller.stop()
        return

