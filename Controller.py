
class Controller:
    def __init__(self, engine):
        self.engine = engine
        self.view = None

    def get_planets_number(self):
        return self.engine.NBR_PLANETES

    def get_coords(self):
        return self.engine.get_coords()

    def get_engine_size(self):
        return self.engine.SIZE_X,self.engine.SIZE_Y,self.engine.SIZE_Z

    def update_pos(self):
        self.engine.timestep()

    def set_view(self, view):
        self.view = view

    def set_theta_value(self, value):
        self.engine.THETA = value

    def get_theta_parameter(self):
        return self.engine.THETA

    def run(self):
        self.view.run()

    def stop(self):
        self.view.exitFunc()
