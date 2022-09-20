import sys
sys.path.append(r"..")
from components import Lens, DoubleDeflector, Aperture, Sample
from model import buildmodel
from main import run_pyqt

components = [Lens(name = '1st Condenser Lens', z = 1.5, f = -0.05),
              Aperture(name = 'Spray Aperture', z = 1.2, aperture_radius_inner = 0.05),
              Lens(name = '2nd Condenser Lens', z = 1.0, f = -0.15),
              DoubleDeflector(name = 'Deflection Coils', z_up = 0.8, z_low = 0.7),
              Lens(name = 'Objective Lens', z = 0.5, f = -0.3),
              Aperture(name = 'Objective Aperture', z = 0.4, aperture_radius_inner = 0.05),
              Sample(name = 'Sample', z = 0.1)
              ]

model = buildmodel(components, beam_z = 1.7, beam_type = 'point', 
                   num_rays = 64, beam_semi_angle = 0.15)
run_pyqt(model)

