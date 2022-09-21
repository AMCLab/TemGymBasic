import sys
sys.path.append(r"..")
from components import Lens, Quadrupole, DoubleDeflector, Aperture
from model import Model
from run import run_pyqt

components = [Lens(name = 'Electrostatic Lens', z = 3, f = -0.2),
              DoubleDeflector(name = 'Gun Beam Deflectors', z_up = 2.8, z_low = 2.7),
              Lens(name = '1st Condenser Lens', z = 2.6, f = -0.2),
              Lens(name = '2nd Condenser Lens', z = 2.5, f = -0.2),
              Aperture(name = 'Condenser Aperture', z = 2.3),
              Quadrupole(name = 'Condenser Stig', z = 2.2),
              DoubleDeflector(name = 'Condenser Deflectors', z_up = 2.1, z_low = 2.0),
              Lens(name = 'Condenser Mini Lens', z = 1.8, f = -0.2),
              Aperture(name = 'Objective Aperture', z = 1.7),
              Lens(name = 'Objective Lens', z = 1.5, f = -0.2),
              Quadrupole(name = 'Objective Stig', z = 1.4),
              Lens(name = 'Objective Mini Lens', z = 1.3, f = -0.2),
              DoubleDeflector(name = 'Image Shifts', z_up = 1.1, z_low = 1.0),
              Aperture(name = 'Selected Area Aperture', z = 0.9),
              Quadrupole(name = 'Intermediate Lens Stigmator', z = 0.8),
              Lens(name = '1st Intermediate Lens', z = 0.7, f = -0.2),
              Lens(name = '2nd Intermediate Lens', z = 0.6, f = -0.2),
              Lens(name = '3rd Intermediate Lens', z = 0.5, f = -0.2),
              DoubleDeflector(name = 'Projector Lens Deflectors', z_up = 0.4, z_low = 0.3),
              Lens(name = 'Projector Lens', z =0.2, f = -0.2)
              ]

model_ = Model(components, beam_z = 3.5, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
run_pyqt(model_)
    
