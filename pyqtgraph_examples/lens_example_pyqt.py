import os
os.chdir(r'G:\My Drive\Davids Research\LinearTEM\LINEARTEMGYM-master_\LINEARTEMGYM-master\temgym\src')
from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from PyQt5.QtWidgets import QApplication
import sys 


def main():
    components = [comp.Lens(name = 'Lens', z = 0.5, f = -0.5)]
    
    model_ = Model(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.15)
    
    viewer = run_pyqt(model_)   
    
    return viewer 

if __name__ == '__main__':
    
    AppWindow = QApplication(sys.argv)
    
    viewer = main()
    
    #Show the viewer
    viewer.show()
    
    AppWindow.exec_()