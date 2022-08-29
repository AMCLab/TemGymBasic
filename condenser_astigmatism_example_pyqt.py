from components import AstigmaticLens, Quadrupole
from model import buildmodel
from main import run_pyqt

components = [Quadrupole(name = 'Condenser Stigmator', z = 0.7),
              AstigmaticLens(name = 'Condenser Lens', z = 0.5, fx = -0.4, fy = -0.6)]

model = buildmodel(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
run_pyqt(model)