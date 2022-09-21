import sys
sys.path.append(r"..")
from components import Lens
from model import Model
from run import run_pyqt

components = [Lens(name = 'Lens', z = 0.5, f = -0.5)]

model_ = Model(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.15)
run_pyqt(model_)    
