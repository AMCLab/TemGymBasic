import sys
from PyQt5.QtWidgets import QApplication
sys.path.append(r"..")
from components import Lens, Aperture
from model import Model
from run import run_pyqt

def main():
    components = [Aperture(name = 'Condenser Aperture', z = 0.3, x = 0.04, y = 0, aperture_radius_inner = 0.055),
                  Lens(name = 'Condenser Lens', z = 0.2, f = -0.5)]
    
    model_ = Model(components, beam_z = 0.8, beam_type = 'point', num_rays = 1024, beam_semi_angle = 0.21)
    run_pyqt(model_)
    
if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    main()
    sys.exit(AppWindow.exec_())