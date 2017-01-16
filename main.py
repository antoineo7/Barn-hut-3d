from Controller import *
from utils import *
from Engine import *
from View import *

engine = Engine(read_params("default"))
controller = Controller(engine)
#view2 = View2(controller)

view = View(controller,from_file=True, file_name='simulation/easytry.txt')

controller.set_view(view)
controller.run()



