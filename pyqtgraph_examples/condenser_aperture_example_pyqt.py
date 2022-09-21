import sys
sys.path.append(r"..")
from components import Lens, Aperture
from model import Model
from run import run_pyqt

components = [Aperture(name = 'Condenser Aperture', z = 0.3, x = 0.25, y = 0),
              Lens(name = 'Condenser Lens', z = 0.2, f = -0.5)]

model_ = Model(components, beam_z = 0.8, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
run_pyqt(model_)
    