
from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from temgymbasic.functions import make_test_sample
from PyQt5.QtWidgets import QApplication
import os
import sys 

def main():
    sample = make_test_sample()

    detector_pixels = 256
    detector_pixel_size = 0.000050 #pixel size in metres
    detector_width = detector_pixels * detector_pixel_size
    
    scan_pixels = 128
    sample_pixel_size = 0.000001 #for now assume square sample
    sample_width = scan_pixels * sample_pixel_size
    
    camera_length = 0.15
    overfocus = 0.001
    semiconv = 0.02
    
    components = [comp.DoubleDeflector(name = 'Scan Coils', z_up = 0.3, z_low = 0.25),
                  comp.Lens(name = 'Lens', z = 0.20, f = -0.05),
                  comp.Sample(name = 'Sample', sample = sample, z = camera_length, width = sample_width),
                  comp.DoubleDeflector(name = 'Descan Coils', z_up = 0.1, z_low = 0.09)
                  ]
    
    model = Model(components, semiconv, overfocus, beam_z = 0.4, beam_type = 'paralell', num_rays = 2**12, 
                  experiment = '4DSTEM', detector_pixels = detector_pixels, 
                   detector_size = detector_width)
    
    #Setting overfocus

    
    viewer = run_pyqt(model)  
    
    print(model.beam_radius)
    
    return viewer 

if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    viewer = main()   
    viewer.show() 
    AppWindow.exec_()
