from components import Biprism
from model import buildmodel
from main import run_pyqt

components = [Biprism(name = 'Biprism', z = 0.7)]

model = buildmodel(components, beam_z = 0.3, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
run_pyqt(model)