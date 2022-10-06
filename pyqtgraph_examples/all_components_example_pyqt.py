from components import (Lens, Deflector, DoubleDeflector, Biprism, Aperture,
                        AstigmaticLens, Quadrupole)
from run import run_pyqt
from model import Model
import sys
sys.path.append(r"..")

#Create List of Components
components = [AstigmaticLens(name='Astigmatic Lens', z=1.2),
              Lens(name='Lens', z=1.0),
              Quadrupole(name='Quadrupole', z=0.9),
              DoubleDeflector(name='Double Deflector', z_up=0.70, z_low=0.65),
              Deflector(name='Deflector', z=0.6, defx=0, defy=0),
              Biprism(name='Biprism', z=0.4),
              Aperture(name='Aperture', z=0.1, aperture_radius_inner=0.05)]

#Generate TEM Model
model_ = Model(components, beam_z=1.5, beam_type='point',
               num_rays=32, beam_semi_angle=0.03)

#Run Pyqtgraph Interface
run_pyqt(model_)
