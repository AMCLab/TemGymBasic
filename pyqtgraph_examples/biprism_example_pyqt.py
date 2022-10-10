from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from PyQt5.QtWidgets import QApplication
import sys 

def main():
    components = [comp.Biprism(name = 'Condenser Biprism', z = 0.7),
                  comp.Sample(name = 'Sample', z = 0.5, width = 0.2),
                  comp.Biprism(name = 'Biprism 1', z = 0.4),
                  comp.Biprism(name = 'Biprism 2', z = 0.2)]

    model_ = Model(components, beam_z = 1.0, beam_type = 'point', num_rays = 4096, beam_semi_angle = 0.1)
    run_pyqt(model_)

if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    main()
    sys.exit(AppWindow.exec_())


