
import sys
sys.path.append(r"..")

from components import (Lens, Deflector, DoubleDeflector, Biprism, Aperture, 
                        AstigmaticLens, Quadrupole)

from model import Model
import numpy as np
from run import show_matplotlib

#Create List of Components
components = [Lens(name='Lens', z=0.85),
              AstigmaticLens(name='Astigmatic Lens', z=0.7),
              Quadrupole(name='Quadrupole', z=0.63),
              DoubleDeflector(name='Double Deflector', z_up=0.5, z_low=0.45),
              Deflector(name='Single Deflector', z=0.3, defx=0, defy=0),
              Biprism(name='Biprism', z=0.2, theta = np.pi/2, deflection = 0.2),
              Aperture(name='Aperture', z=0.10, aperture_radius_inner=0.05)]

#Generate TEM Model
model_ = Model(components, beam_z=1, beam_type='x_axial',
                   num_rays=32, beam_semi_angle=0.15)

#Save Figure with Matplotlib
fig, ax = show_matplotlib(model_, name = 'all_components.svg', label_fontsize = 18)
fig.savefig('all_components.svg', dpi = 500)
