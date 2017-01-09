from Controller import *
from utils import *


engine = Engine(read_params("default"))
view = View(engine, from_file=True, file_name='simulation/circle2kvit.txt')
app = Controller(engine, view)
app.run()

