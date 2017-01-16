import easygui
from Controller import *
from utils import *
from Engine import *
from View import *
import os

mode = easygui.buttonbox('Choose your mode', 'N Body Simulator', ('Live', 'PreCalc','Quick Simul'))
if mode == 'Quick Simul':
    engine = Engine(read_params("default"))
    controller = Controller(engine)
    view = View(controller)
    controller.set_view(view)
    controller.run()

if mode is None:
    exit()
if mode == 'Live':
    nbr_bodies = easygui.integerbox("Choose bodies amount",lowerbound=1,upperbound=10000)
    theta = easygui.integerbox("Choose 10 theta", lowerbound=0, upperbound=10)/10.0
    write_to_file = easygui.ynbox('Do You want to save simulation ?', 'N Body Simulator', ('Yes', 'No'))
    if write_to_file:
        loop = True
        while loop:
            file_name = "simulation/"+ easygui.enterbox("Choose file name")
            if file_name[11:] in os.listdir('simulation/'):
                loop = not easygui.ynbox("This file already exists. Do you want to overwrite file ?")
            else :
                loop = False
        section_name = file_name[11:]

    else:
        file_name = None
        section_name = "Section easygui"
    create_ini_section(section_name, nbr_bodies, theta)
    engine = Engine(read_params(section_name),write_to_file=write_to_file,file_name=file_name)
    controller = Controller(engine)
    view = View(controller)
    controller.set_view(view)
    controller.run()
if mode == 'PreCalc':
    file_name = 'simulation/'+easygui.choicebox(msg='Choose File',choices=[file_name for file_name in os.listdir('simulation/') if file_name[-4:]=='.txt'])
    engine = Engine(read_params("default"))
    controller = Controller(engine)
    view = View(controller, from_file=True, file_name=file_name)
    controller.set_view(view)
    controller.run()