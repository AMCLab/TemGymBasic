import sys
sys.path.append(r"..")
from components import Lens, Aperture
from model import Model
from run import run_pyqt

components = [Aperture(name = 'Condenser Aperture', z = 0.3, x = 0, y = 0, aperture_radius_inner = 0.1),
              Lens(name = 'Condenser Lens', z = 0.2, f = -0.5)]

model_ = Model(components, beam_z = 0.8, beam_type = 'point', num_rays = 512, beam_semi_angle = 0.2)
run_pyqt(model_)
    