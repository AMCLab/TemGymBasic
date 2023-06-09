from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from PyQt5.QtWidgets import QApplication
import sys 

def main():
    #Create List of Components
    components = [comp.AstigmaticLens(name='Astigmatic Lens', z=1.2),
                comp.Lens(name='Lens', z=1.0),
                comp.Quadrupole(name='Quadrupole', z=0.9),
                comp.DoubleDeflector(name='Double Deflector', z_up=0.70, z_low=0.65),
                comp.Deflector(name='Deflector', z=0.6, defx=0, defy=0),
                comp.Biprism(name='Biprism', z=0.4),
                comp.Aperture(name='Aperture', z=0.1, aperture_radius_inner=0.05)]

    #Generate TEM Model
    model_ = Model(components, beam_z=1.5, beam_type='point',
                num_rays=32, gun_beam_semi_angle=0.03)
    
    viewer = run_pyqt(model_)  
    
    return viewer 

if __name__ == '__main__':
    
    AppWindow = QApplication(sys.argv)
    viewer = main()  
    viewer.show()  
    AppWindow.exec_()
