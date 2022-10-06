import sys
from PyQt5.QtWidgets import QApplication
sys.path.append(r"..")
from components import Lens, DoubleDeflector, Sample
from model import Model
from run import run_pyqt

def main():
    #Create List of Components
    components = [Lens(name = 'Condenser Lens', z = 1.2, f = -0.1),
                  DoubleDeflector(name = 'Double Deflector', z_up = 0.9, z_low = 0.8),
                  Lens(name = 'Objective Lens', z = 0.6, f = -0.1),
                  Sample(name = 'Sample', z = 0.5),
                  Lens(name = 'Intermediate Lens', z = 0.4, f = -0.5),
                  Lens(name = 'Projector Lens', z = 0.1, f = -0.5)]
    
    #Generate Model
    model_ = Model(components, beam_z = 1.5, beam_type = 'point', num_rays = 128, beam_semi_angle = 0.03)
    
    
    run_pyqt(model_)

if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    main()
    sys.exit(AppWindow.exec_())
        
