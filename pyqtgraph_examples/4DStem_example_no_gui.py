
from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from temgymbasic.functions import make_test_sample
from PyQt5.QtWidgets import QApplication
import os
import sys 

sample = make_test_sample()


components = [comp.DoubleDeflector(name = 'Scan Coils', z_up = 0.81, z_low = 0.70),
              comp.Lens(name = 'Lens', z = 0.60, f = -0.05),
              comp.Sample(name = 'Sample', sample = sample, z = 0.5),
              comp.DoubleDeflector(name = 'Descan Coils', z_up = 0.4, z_low = 0.3)
              ]

model_ = Model(components, beam_z = 1.0, beam_type = 'paralell', num_rays = 2**12, gun_beam_semi_angle = 0.05, beam_radius = 0.02, experiment = '4DSTEM')


