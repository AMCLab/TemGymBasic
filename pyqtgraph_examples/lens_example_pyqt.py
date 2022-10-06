import sys
from PyQt5.QtWidgets import QApplication
sys.path.append(r"..")
from components import Lens
from model import Model
from run import run_pyqt

def main():
    components = [Lens(name = 'Lens', z = 0.5, f = -0.5)]
    
    model_ = Model(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.15)
    run_pyqt(model_)    

if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    main()
    sys.exit(AppWindow.exec_())