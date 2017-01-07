import tkinter as tk
from random import *
from math import *
import numpy as np

#  ------Constants----------
SIZE_X = 1300
SIZE_Y = 600
MASSE_MIN = 1000
MASSE_MAX = 10000
TAILLE_MIN = 3
TAILLE_MAX = 7
THETA = 0.5
G = 0.1
VITESSE_MIN = 0.00
VITESSE_MAX = 0.0
dt = 0.1
RAYON_POS_INI = min(SIZE_Y,SIZE_X)/ 2
NBR_PLANETES = 150
EPSILON = 2

# ------Graphics-Initialisation----
fenetre = tk.Tk()
canvas = tk.Canvas(fenetre, height=SIZE_Y, width=SIZE_X, bg="black")
canvas.pack()
quit = tk.Button(fenetre, text='Quitter', command=fenetre.quit)
quit.pack()


# -------Classes---------------
class Body:
    def __init__(self, x, y, m, vx, vy):
        self.x = x
        self.y = y
        self.m = m
        self.fx = 0
        self.fy = 0
        self.vx = vx
        self.vy = vy
        self.cercle = None

    def get_cercle(self):
        return self.cercle

    def get_coord(self):
        return self.x, self.y

    def get_mass(self):
        return self.m

    def description(self):
        print("Ce Body a pour coordonnées ", (self.x, self.y), " et une masse de ", self.m, ".")

    def is_in_quad(self, quad):
        xq, yq = quad.get_coord()
        sxq,syq = quad.get_size()
        if self.y >= yq and not self.x < xq <= xq + sxq and self.y <= yq + syq:
            return True
        else:
            return False

    def which_subquad(self, quad):
        subs = quad.subdivise()
        for k in range(4):
            if self.is_in_quad(subs[k]):
                return ["NW", "NE", "SW", "SE"][k], subs[k]

    def ini_graph(self):
        global canvas
        demi_rayon = 0.5 * ((TAILLE_MAX - TAILLE_MIN) * ((self.m - MASSE_MIN) / (MASSE_MAX - MASSE_MIN)) + TAILLE_MIN)
        self.cercle = canvas.create_oval(self.x - demi_rayon, self.y - demi_rayon, self.x + demi_rayon,
                                         self.y + demi_rayon,
                                         fill="white")
        pass

    def show_force(self):
        global canvas
        canvas.create_line(self.x, self.y, self.x + 1000 * self.fx, self.y + 1000 * self.fy, arrow=tk.LAST, fill="red")

    def get_dist(self, body2):
        x2, y2 = body2.get_coord()
        return sqrt((self.x - x2) ** 2 + (self.y - y2) ** 2)

    def get_force(self):
        return self.fx, self.fy

    def force_caused_by(self, body2):
        global EPSILON
        global G
        x2, y2 = body2.get_coord()
        d = self.get_dist(body2)
        if d != 0:
            F = G * self.get_mass() * body2.get_mass() / ((d + EPSILON) ** 2)
        else:
            F = 0
        return F * (x2 - self.x) / (d + EPSILON), F * (y2 - self.y) / (d + EPSILON)

    def act_forces_vit_pos_rec(self, tab):
        global THETA
        if tab[0] is None and tab[2] == {}:
            return
        if not (tab[0] is None) and tab[0] != self:
            fx1, fy1 = self.force_caused_by(tab[0])
            self.fx += fx1
            self.fy += fy1
            return
        sx,sy = tab[1].get_size()
        bodyeq = Body(tab[4][0], tab[4][1], tab[3], 0, 0)
        d = self.get_dist(bodyeq)
        if d != 0:
            if min(sx,sy) / d < THETA:
                fx1, fy1 = self.force_caused_by(bodyeq)
                self.fx += fx1
                self.fy += fy1
            else:
                for key in ["NW", "NE", "SW", "SE"]:
                    self.act_forces_vit_pos_rec(tab[2][key])
        return

    def act_forces_vit_pos(self, quadtree):
        """

        :type quadtree: Quadtree
        """
        global TAILLE_MIN
        global TAILLE_MAX
        global MASSE_MAX
        global MASSE_MIN
        global canvas
        global dt
        self.fx = 0
        self.fy = 0
        self.act_forces_vit_pos_rec(quadtree.tree)
        self.vx += self.fx * dt / self.m
        self.vy += self.fy * dt / self.m
        self.x += self.vx * dt
        self.y += self.vy * dt
        demi_rayon = 0.5 * ((TAILLE_MAX - TAILLE_MIN) * ((self.m - MASSE_MIN) / (MASSE_MAX - MASSE_MIN)) + TAILLE_MIN)
        canvas.coords(self.cercle, self.x - demi_rayon, self.y - demi_rayon, self.x + demi_rayon, self.y + demi_rayon)
        pass

    def is_in_ecran(self):
        return self.is_in_quad(Quadrant(0, 0, SIZE_X, SIZE_Y))


class Quadrant:
    def __init__(self, x, y, lx, ly):
        self.x_upleft = x
        self.y_upleft = y
        self.size_x = lx
        self.size_y = ly

    def get_coord(self):
        return self.x_upleft, self.y_upleft

    def get_size(self):
        return self.size_x, self.size_y

    def subdivise(self):
        lx2 = self.size_x / 2
        ly2 = self.size_y / 2
        x2 = self.x_upleft + lx2
        y2 = self.y_upleft + ly2
        return [Quadrant(self.x_upleft, self.y_upleft, lx2, ly2), Quadrant(x2, self.y_upleft, lx2, ly2),
                Quadrant(self.x_upleft, y2, lx2, ly2), Quadrant(x2, y2, lx2, ly2)]

    def description(self):
        print("Ce Quadrant a pour coordonnees ", (self.x_upleft, self.y_upleft), " et une longueur de ", self.size_x, self.size_y, ".")
        pass

    def ini_graph(self):
        global canvas
        canvas.create_rectangle(self.x_upleft, self.y_upleft, self.x_upleft + self.size_x, self.y_upleft + self.size_y,
                                outline="green")
        pass


class Quadtree:
    def __init__(self, root_quad):
        self.tree = [None, root_quad, {}, 0, (None, None)]  # [body,quad,subdivisions,total mass,center of mass]
        self.quadleaf = []
        self.bodyleaf = []

    def add_body_rec(self, body, tab):
        if tab[0] is None and tab[2] == {}:
            self.quadleaf.append(tab[1])
            return [body, tab[1], {}, body.get_mass(), body.get_coord()]
        lbl1, subquad1 = body.which_subquad(tab[1])
        x, y = body.get_coord()
        m = body.get_mass()
        tab[4] = ((tab[4][0] * tab[3] + x * m) / (tab[3] + m), (tab[4][1] * tab[3] + y * m) / (tab[3] + m))
        tab[3] += body.get_mass()
        if tab[0] is None:
            tab[2][lbl1] = self.add_body_rec(body, tab[2][lbl1])
        else:
            self.quadleaf.remove(tab[1])
            body2 = tab[0]
            tab[0] = None
            subquad = tab[1].subdivise()
            tab[2] = {"NW": [None, subquad[0], {}], "NE": [None, subquad[1], {}], "SW": [None, subquad[2], {}],
                      "SE": [None, subquad[3], {}]}
            lbl2, subquad2 = body2.which_subquad(tab[1])
            tab[2][lbl1] = self.add_body_rec(body, tab[2][lbl1])
            tab[2][lbl2] = self.add_body_rec(body2, tab[2][lbl2])
        return tab

    def add_body(self, body):
        self.bodyleaf.append(body)
        self.tree = self.add_body_rec(body, self.tree)

    def description(self):
        print(self.tree)

    def ini_graph(self):
        for body in self.bodyleaf:
            body.ini_graph()


def gen_rdm_bodies(k):
    global SIZE_X
    global SIZE_Y
    global MASSE_MIN
    global MASSE_MAX
    global RAYON_POS_INI
    planetes = []
    for i in range(k):
        alpha = 2 * pi * random()
        alpha2 = 2 * pi * random()
        v = (VITESSE_MAX - VITESSE_MIN) * random() + VITESSE_MIN
        p = abs(sqrt(RAYON_POS_INI)*np.random.randn())
        print(p)
        planetes.append(
            Body(SIZE_X / 2 + p * cos(alpha2), SIZE_Y / 2 + p * sin(alpha2),
                 (MASSE_MAX - MASSE_MIN) * random() + MASSE_MIN, v * cos(alpha), v * sin(alpha)))
    return planetes


planetes = gen_rdm_bodies(NBR_PLANETES)
Q = Quadrant(0, 0, SIZE_X, SIZE_Y)
arbre = Quadtree(Q)
for planete in planetes:
    arbre.add_body(planete)
arbre.ini_graph()
for planete in planetes:
    planete.show_force()


def act():
    global canvas
    global planetes
    Q = Quadrant(0, 0, SIZE_X, SIZE_Y)
    arbre = Quadtree(Q)
    for planete in planetes:
        if not planete.is_in_ecran():
            planetes.remove(planete)
            canvas.delete(planete.get_cercle())
        else:
            arbre.add_body(planete)
    for planete in planetes:
        planete.act_forces_vit_pos(arbre)
    fenetre.after(1, act)


act()
tk.mainloop()
