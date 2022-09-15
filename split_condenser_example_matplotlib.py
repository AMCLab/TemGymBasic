
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole, Sample
from model import buildmodel
import numpy as np
from main import show_matplotlib

components = [Biprism(name = 'Condenser Biprism', z = 0.7, theta=np.pi/2, width = 0.01),
              Sample(name = 'Sample', z = 0.5, width = 0.2, x = -0.1),
              Biprism(name = 'Biprism 1', z = 0.4, theta=np.pi/2, width = 0.01),
              Biprism(name = 'Biprism 2', z = 0.2, theta=np.pi/2, width = 0.01)]

axis_view = 'x_axial'
model = buildmodel(components, beam_z=1.0, beam_type='x_axial',
                   num_rays=32, beam_semi_angle=0.15)


name = 'split_condenser_biprism.svg'
fig, ax = show_matplotlib(model, name = name)
fig.suptitle('Split Condenser Biprism', fontsize=32)
fig.savefig(name, dpi = 500)



