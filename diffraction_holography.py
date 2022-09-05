from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole
from model import buildmodel
from main import run_pyqt

components = [Lens(name = 'Lens', z = 1.0),
              Aperture(name = 'Double Aperture', z = 0.701, aperture_radius_inner = 0.005),
              Aperture(name = '', z = 0.69, aperture_radius_inner = 0.05)
              ]

model = buildmodel(components, beam_z = 1.5, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
run_pyqt(model)