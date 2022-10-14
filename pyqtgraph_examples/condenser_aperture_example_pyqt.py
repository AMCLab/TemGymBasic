from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from PyQt5.QtWidgets import QApplication
import sys 

def main():
    components = [comp.Aperture(name = 'Condenser Aperture', z = 0.3, x = 0.04, y = 0, aperture_radius_inner = 0.055),
                  comp.Lens(name = 'Condenser Lens', z = 0.2, f = -0.5)]
    
    model_ = Model(components, beam_z = 0.8, beam_type = 'point', num_rays = 1024, beam_semi_angle = 0.21)
    
    viewer = run_pyqt(model_)  
    
    return viewer 

if __name__ == '__main__':
    
    AppWindow = QApplication(sys.argv)
    viewer = main()   
    viewer.show() 
    AppWindow.exec_()