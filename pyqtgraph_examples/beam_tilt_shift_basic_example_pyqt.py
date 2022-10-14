from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from PyQt5.QtWidgets import QApplication
import sys 

def main():
    #Create List of Components
    components = [comp.DoubleDeflector(name = 'Double Deflector', z_up = 0.4, z_low = 0.3),
                  comp.Sample(name = 'Sample', z = 0.2),
                  comp.Lens(name = 'Objective Lens', z = 0.1, f = -0.1)]
    
    #Generate Model
    model_ = Model(components, beam_z = 0.6, beam_type = 'paralell', num_rays = 128)
    
    viewer = run_pyqt(model_)  
    
    return viewer 

if __name__ == '__main__':
    
    AppWindow = QApplication(sys.argv)
    viewer = main()   
    viewer.show() 
    AppWindow.exec_()