
from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from temgymbasic.functions import make_test_sample
from PyQt5.QtWidgets import QApplication
import os
import sys 

def main():
    sample = make_test_sample()

    camera_length = 0.15
    
    components = [comp.DoubleDeflector(name = 'Scan Coils', z_up = 0.8, z_low = 0.7),
                  comp.Lens(name = 'Lens', z = 0.30, f = -0.05),
                  comp.Sample(name = 'Sample', sample = sample, z = camera_length),
                  comp.DoubleDeflector(name = 'Descan Coils', z_up = 0.1, z_low = 0.09)
                  ]
    
    model = Model(components, beam_z = 1, beam_type = 'paralell', num_rays = 2**12, 
                  experiment = '4DSTEM')
    
    viewer = run_pyqt(model)
    
    return viewer 

if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    viewer = main()   
    viewer.show() 
    
    AppWindow.exec_()
