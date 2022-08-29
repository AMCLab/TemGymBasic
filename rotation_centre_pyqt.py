from components import Lens
from model import buildmodel
from main import run_pyqt

components = [Lens(name = 'Lens', z = 0.7)]

model = buildmodel(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
run_pyqt(model)