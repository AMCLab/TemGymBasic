import sys
from PyQt5.QtWidgets import QApplication
sys.path.append(r"..")
from components import Lens, DoubleDeflector, Sample
from model import Model
from run import run_pyqt

def main():
    #Create List of Components
    components = [DoubleDeflector(name = 'Double Deflector', z_up = 0.4, z_low = 0.3),
                  Sample(name = 'Sample', z = 0.2),
                  Lens(name = 'Objective Lens', z = 0.1, f = -0.1)]
    
    #Generate Model
    model_ = Model(components, beam_z = 0.6, beam_type = 'paralell', num_rays = 128)
    
    
    run_pyqt(model_)
        
if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    main()
    sys.exit(AppWindow.exec_())
