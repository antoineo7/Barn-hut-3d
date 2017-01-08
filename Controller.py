from Engine import *
from View import *


class Controller:
    def __init__(self, engine, view):
        self.engine = engine
        self.view = view

    def run(self):
        self.view.run()
