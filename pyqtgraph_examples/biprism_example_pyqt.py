import sys
sys.path.append(r"..")
from components import Biprism, Sample, Aperture
from model import buildmodel
from run import run_pyqt

components = [Biprism(name = 'Condenser Biprism', z = 0.7),
              Sample(name = 'Sample', z = 0.5, width = 0.2),
              Biprism(name = 'Biprism 1', z = 0.4),
              Biprism(name = 'Biprism 2', z = 0.2)]

model = buildmodel(components, beam_z = 1.0, beam_type = 'point', num_rays = 4096, beam_semi_angle = 0.1)
run_pyqt(model)

