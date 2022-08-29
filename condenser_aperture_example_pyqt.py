from components import Lens, Aperture
from model import buildmodel
from main import run_pyqt

components = [Aperture(name = 'Condenser Aperture', z = 0.7),
              Lens(name = 'Condenser Lens', z = 0.5)]

model = buildmodel(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
run_pyqt(model)