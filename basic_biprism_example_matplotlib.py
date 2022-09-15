
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole
from model import buildmodel
from main import show_matplotlib
import numpy as np

components = [Biprism(name='Biprism', z=0.6, theta=np.pi/2, width=0.01),
              Lens(name='Lens', z=0.5, f=-0.1),
              Aperture(name='Aperture', z=0.25, aperture_radius_inner = 0.10)]

axis_view = 'x_axial'
model = buildmodel(components, beam_z=1.0, beam_type='x_axial',
                   num_rays=32, beam_semi_angle=0.15)

name = 'biprism_model.svg'
fig, ax = show_matplotlib(model, name = name)
fig.suptitle('Basic Biprism', fontsize=32)
fig.savefig(name, dpi = 500)




