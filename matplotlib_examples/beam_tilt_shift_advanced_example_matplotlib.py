import sys
sys.path.append(r"..")
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole, Sample
from model import Model
import numpy as np
from run import show_matplotlib

components = [Lens(name = 'Condenser Lens', z = 1.2, f = -0.1),
              DoubleDeflector(name = 'Double Deflector', z_up = 0.9, z_low = 0.8, updefx = 1, lowdefx = -1),
              Lens(name = 'Objective Lens', z = 0.6, f = -0.1),
              Sample(name = 'Sample', z = 0.5),
              Lens(name = 'Intermediate Lens', z = 0.4, f = -0.075),
              Lens(name = 'Projector Lens', z = 0.1, f = -0.1)]

axis_view = 'x_axial'
model_ = Model(components, beam_z=1.5, beam_type='x_axial',
                   num_rays=32, beam_semi_angle=0.15)

name = 'beam_tilt.svg'
fig, ax = show_matplotlib(model_, name = name)
fig.suptitle('Beam Pivot Points', fontsize=32)
fig.savefig(name, dpi = 500)
