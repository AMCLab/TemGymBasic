from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from PyQt5.QtWidgets import QApplication
from temgymbasic.functions import make_test_sample
import sys 

def main():

    sample = make_test_sample()

    #Create List of Components
    components = [comp.Lens(name = 'Condenser Lens', z = 1.2, f = -0.1),
                  comp.DoubleDeflector(name = 'Double Deflector', z_up = 0.9, z_low = 0.8),
                  comp.Lens(name = 'Objective Lens', z = 0.6, f = -0.1),
                  comp.Sample(name = 'Sample', sample = sample, z = 0.5),
                  comp.Lens(name = 'Intermediate Lens', z = 0.4, f = -0.5),
                  comp.Lens(name = 'Projector Lens', z = 0.1, f = -0.5)]
    
    #Generate Model
    model_ = Model(components, beam_z = 1.5, beam_type = 'point', num_rays = 128, gun_beam_semi_angle = 0.03)
    
    viewer = run_pyqt(model_)  

    return viewer 

if __name__ == '__main__':
    
    AppWindow = QApplication(sys.argv)
    viewer = main()    
    viewer.show()
    AppWindow.exec_()
