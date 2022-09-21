import sys
sys.path.append(r"..")
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole
from model import buildmodel
from run import run_pyqt

components = [Lens(name = 'Lens', z = 0.5)]

model = buildmodel(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.15)
run_pyqt(model)    
