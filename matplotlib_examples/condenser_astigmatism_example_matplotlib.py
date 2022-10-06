import sys
sys.path.append(r"..")
from components import AstigmaticLens, Quadrupole
from model import Model
import numpy as np
from run import show_matplotlib


components = [
    AstigmaticLens(name='Condenser Lens', z=0.7, fx=-0.4, fy=-0.6),
    Quadrupole(name='Condenser Stigmator', z=0.5)
]

axis_view = 'x_axial'
model_ = Model(components, beam_z=1.0, beam_type='x_axial',
                   num_rays=32, beam_semi_angle=0.15)

name = 'condenser_astigmatism.svg'
fig, ax = show_matplotlib(model_, name = name)
fig.suptitle('Condenser Astigmatism', fontsize=32)
fig.savefig(name, dpi = 500)
