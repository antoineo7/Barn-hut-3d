from random import *
from math import *
import numpy as np


class Body:
    def __init__(self, x, y, z, m, vx, vy, vz, engine):
        self.x = x
        self.y = y
        self.z = z
        self.m = m
        self.fx = 0
        self.fy = 0
        self.fz = 0
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.engine = engine

    def get_coord(self):
        return self.x, self.y, self.z

    def get_mass(self):
        return self.m

    def description(self):
        print("Ce Body a pour coordonnees ", (self.x, self.y, self.z), " et une masse de ", self.m, ".")

    def is_in_quad(self, quad):
        xq, yq, zq = quad.get_coord()
        sxq, syq, szq = quad.get_size()
        if self.y >= yq and not self.x < xq <= xq + sxq and self.y <= yq + syq and self.z>=zq and self.z<=zq+szq:
            return True
        else:
            return False

    def which_subquad(self, quad):
        subs = quad.subdivise()
        for k in range(8):
            if self.is_in_quad(subs[k]):
                return ["NWF", "NEF", "SWF", "SEF", "NWB", "NEB", "SWB", "SEB"][k], subs[k]

    def get_dist(self, body2):
        x2, y2, z2 = body2.get_coord()
        return sqrt((self.x - x2) ** 2 + (self.y - y2) ** 2 + (self.z - z2) ** 2)

    def get_force(self):
        return self.fx, self.fy, self.fz

    def force_caused_by(self, body2):
        x2, y2, z2 = body2.get_coord()
        d = self.get_dist(body2)
        if d != 0:
            F = self.engine.G * self.get_mass() * body2.get_mass() / ((d + self.engine.EPSILON) ** 2)
        else:
            F = 0
        return F * (x2 - self.x) / (d + self.engine.EPSILON), F * (y2 - self.y) / (d + self.engine.EPSILON), F * (z2 - self.z) / (d + self.engine.EPSILON)

    def act_forces_vit_pos_rec(self, tab):
        if tab[0] is None and tab[2] == {}:
            return
        if not (tab[0] is None) and tab[0] != self:
            fx1, fy1, fz1 = self.force_caused_by(tab[0])
            self.fx += fx1
            self.fy += fy1
            self.fz += fz1
            return
        sx, sy, sz = tab[1].get_size()
        bodyeq = Body(tab[4][0], tab[4][1], tab[4][2], tab[3], 0, 0, 0,self.engine)
        d = self.get_dist(bodyeq)
        if d != 0:
            if min(sx,sy,sz) / d < self.engine.THETA:
                fx1, fy1, fz1 = self.force_caused_by(bodyeq)
                self.fx += fx1
                self.fy += fy1
                self.fz += fz1
            else:
                for key in ["NWF", "NEF", "SWF", "SEF", "NWB", "NEB", "SWB", "SEB"]:
                    self.act_forces_vit_pos_rec(tab[2][key])
        return

    def act_forces_vit_pos(self, quadtree):
        """

        :type quadtree: Octree
        """
        self.fx = 0
        self.fy = 0
        self.fz = 0
        self.act_forces_vit_pos_rec(quadtree.tree)
        self.vx += self.fx * self.engine.DT / self.m
        self.vy += self.fy * self.engine.DT / self.m
        self.vz += self.fz * self.engine.DT / self.m
        self.x += self.vx * self.engine.DT
        self.y += self.vy * self.engine.DT
        self.z += self.vz * self.engine.DT

    def is_in_ecran(self):
        return self.is_in_quad(Octant(0, 0, 0, self.engine.SIZE_X, self.engine.SIZE_Y, self.engine.SIZE_Z, self.engine))


class Octant:
    def __init__(self, x, y, z, lx, ly, lz, engine):
        self.x_upleft = x
        self.y_upleft = y
        self.z_upleft = z
        self.size_x = lx
        self.size_y = ly
        self.size_z = lz
        self.engine = engine

    def get_coord(self):
        return self.x_upleft, self.y_upleft, self.z_upleft

    def get_size(self):
        return self.size_x, self.size_y, self.size_z

    def subdivise(self):
        lx2 = self.size_x / 2.0
        ly2 = self.size_y / 2.0
        lz2 = self.size_z / 2.0
        x2 = self.x_upleft + lx2
        y2 = self.y_upleft + ly2
        z2 = self.z_upleft + lz2
        return [Octant(self.x_upleft, self.y_upleft, self.z_upleft, lx2, ly2, lz2, self.engine),
                Octant(x2, self.y_upleft, self.z_upleft, lx2, ly2, lz2, self.engine),
                Octant(self.x_upleft, y2, self.z_upleft, lx2, ly2, lz2, self.engine),
                Octant(x2, y2, self.z_upleft, lx2, ly2, lz2, self.engine),
                Octant(self.x_upleft, self.y_upleft, z2, lx2, ly2, lz2, self.engine),
                Octant(x2, self.y_upleft, z2, lx2, ly2, lz2, self.engine),
                Octant(self.x_upleft, y2, z2, lx2, ly2, lz2, self.engine),
                Octant(x2, y2, z2, lx2, ly2, lz2, self.engine)]

    def description(self):
        print("Ce Octant a pour coordonnees ", (self.x_upleft, self.y_upleft,self.z_upleft), " et une longueur de ",
              self.size_x, self.size_y, self.size_z, ".")
        pass


class Octree:
    def __init__(self, root_quad, engine):
        self.tree = [None, root_quad, {}, 0, (None, None)]  # [body,quad,subdivisions,total mass,center of mass]
        self.quadleaf = []
        self.bodyleaf = []
        self.engine = engine

    def add_body_rec(self, body, tab):
        if tab[0] is None and tab[2] == {}:
            self.quadleaf.append(tab[1])
            return [body, tab[1], {}, body.get_mass(), body.get_coord()]
        lbl1, subquad1 = body.which_subquad(tab[1])
        x, y, z = body.get_coord()
        m = body.get_mass()
        tab[4] = ((tab[4][0] * tab[3] + x * m) / (tab[3] + m),
                  (tab[4][1] * tab[3] + y * m) / (tab[3] + m),
                  (tab[4][2] * tab[3] + z * m) / (tab[3] + m))
        tab[3] += body.get_mass()
        if tab[0] is None:
            tab[2][lbl1] = self.add_body_rec(body, tab[2][lbl1])
        else:
            self.quadleaf.remove(tab[1])
            body2 = tab[0]
            tab[0] = None
            subquad = tab[1].subdivise()
            tab[2] = {"NWF": [None, subquad[0], {}], "NEF": [None, subquad[1], {}], "SWF": [None, subquad[2], {}],
                      "SEF": [None, subquad[3], {}],
                      "NWB": [None, subquad[4], {}], "NEB": [None, subquad[5], {}], "SWB": [None, subquad[6], {}],
                      "SEB": [None, subquad[7], {}]
                      }
            lbl2, subquad2 = body2.which_subquad(tab[1])
            tab[2][lbl1] = self.add_body_rec(body, tab[2][lbl1])
            tab[2][lbl2] = self.add_body_rec(body2, tab[2][lbl2])
        return tab

    def add_body(self, body):
        self.bodyleaf.append(body)
        self.tree = self.add_body_rec(body, self.tree)

    def description(self):
        print(self.tree)


class Engine:
    def __init__(self, params,write_to_file=False,file_name=None):
        SIZE_X, SIZE_Y, SIZE_Z, MASSE_MIN, MASSE_MAX, TAILLE_MIN, TAILLE_MAX \
            , G, VITESSE_MIN, VITESSE_MAX, DT, EPSILON, NBR_PLANETES, THETA = params

        self.SIZE_X = SIZE_X
        self.SIZE_Y = SIZE_Y
        self.SIZE_Z = SIZE_Z
        self.MASSE_MIN = MASSE_MIN
        self.MASSE_MAX = MASSE_MAX
        self.TAILLE_MIN = TAILLE_MIN
        self.TAILLE_MAX = TAILLE_MAX
        self.THETA = THETA
        self.G = G
        self.VITESSE_MIN = VITESSE_MIN
        self.VITESSE_MAX = VITESSE_MAX
        self.DT = DT
        self.RAYON_POS_INI = min(SIZE_Y, SIZE_X, SIZE_Z) / 10
        self.NBR_PLANETES = NBR_PLANETES
        self.EPSILON = EPSILON
        self.planetes = []
        self.write_to_file = write_to_file
        if file_name is None:
            self.file = None
        else:
            self.file = open(file_name, 'w')

        for i in range(self.NBR_PLANETES):
            theta = 2 * pi * random()
            phi = pi * random()
            theta2 = 2 * pi * random()
            phi2 = pi * random()
            v = (self.VITESSE_MAX - self.VITESSE_MIN) * random() + self.VITESSE_MIN
            #p = abs(sqrt(self.RAYON_POS_INI) * np.random.randn())
            p = sqrt(self.RAYON_POS_INI)
            self.planetes.append(
                Body(self.SIZE_X / 2 + p * cos(theta2) * sin(phi2), self.SIZE_Y / 2 + p * sin(theta2) * sin(phi2),
                     self.SIZE_Z / 2 + p * cos(phi2),
                     (self.MASSE_MAX - self.MASSE_MIN) * random() + self.MASSE_MIN, v * cos(theta) * sin(phi),
                     v * sin(theta) * sin(phi),
                     v * cos(phi), self))
        self.quadtree = Octree(Octant(0, 0, 0, self.SIZE_X, self.SIZE_Y, self.SIZE_Z, self), self)
        for planete in self.planetes:
            self.quadtree.add_body(planete)

    def timestep(self):
        self.quadtree = Octree(Octant(0, 0, 0, self.SIZE_X, self.SIZE_Y, self.SIZE_Z, self), self)
        for planete in self.planetes:
            if not planete.is_in_ecran():
                self.planetes.remove(planete)
            else:
                self.quadtree.add_body(planete)
        for planete in self.planetes:
            planete.act_forces_vit_pos(self.quadtree)
        if self.write_to_file:
            s = self.get_coords()
            string = ""
            for tuple in s:
                string += str(tuple)[1:-1] + ";"
            self.file.write(string + "\n")

    def get_coords(self):
        return [planete.get_coord() for planete in self.planetes]


if __name__=="__main__":
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
    dt = 0.1
    NBR_PLANETES = 100
    EPSILON = 2
    engine = Engine(SIZE_X, SIZE_Y, SIZE_Z,
                    MASSE_MIN, MASSE_MAX, TAILLE_MIN, TAILLE_MAX,
                    THETA, G, VITESSE_MIN, VITESSE_MAX, dt, NBR_PLANETES, EPSILON)
    print engine.get_coords()
    engine.timestep()
    print engine.get_coords()


