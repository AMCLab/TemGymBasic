import sys
from PyQt5.QtWidgets import QApplication
sys.path.append(r"..")
from components import AstigmaticLens, Quadrupole
from model import Model
from run import run_pyqt

def main():
    components = [
        AstigmaticLens(name='Condenser Lens', z=0.7, fx=-0.4, fy=-0.6),
        Quadrupole(name='Condenser Stigmator', z=0.5)
    ]
    
    model_ = Model(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
    run_pyqt(model_)

if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    main()
    sys.exit(AppWindow.exec_())
