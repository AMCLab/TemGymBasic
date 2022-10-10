from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from PyQt5.QtWidgets import QApplication
import sys 

def main():
    components = [comp.Lens(name = 'Lens', z = 0.5, f = -0.5)]
    
    model_ = Model(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.15)
    run_pyqt(model_)    

if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    main()
    sys.exit(AppWindow.exec_())