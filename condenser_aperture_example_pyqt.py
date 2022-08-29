from components import Lens, Aperture
from model import buildmodel
from main import run_pyqt

components = [Aperture(name = 'Condenser Aperture', z = 0.3),
              Lens(name = 'Condenser Lens', z = 0.2)]

model = buildmodel(components, beam_z = 0.8, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
run_pyqt(model)