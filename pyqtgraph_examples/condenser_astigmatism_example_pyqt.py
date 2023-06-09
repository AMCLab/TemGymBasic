from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from PyQt5.QtWidgets import QApplication
import sys 

def main():
    components = [
        comp.AstigmaticLens(name='Condenser Lens', z=0.7, fx=-0.4, fy=-0.6),
        comp.Quadrupole(name='Condenser Stigmator', z=0.5)
    ]
    
    model_ = Model(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, gun_beam_semi_angle = 0.03)
    
    viewer = run_pyqt(model_)  

    return viewer 

if __name__ == '__main__':
    
    AppWindow = QApplication(sys.argv)
    viewer = main()    
    viewer.show()
    AppWindow.exec_()
