from Controller import *
from utils import *
from Engine import *
from View import *

engine = Engine(read_params("default"))
controller = Controller(engine)
view2 = View2(controller)

#view = View(controller,from_file=False, file_name='simulation/Nuit1.txt')

controller.set_view(view2)
controller.run()
print("ok")


