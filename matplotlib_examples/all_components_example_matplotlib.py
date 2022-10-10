
from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import show_matplotlib
import numpy as np

#Create List of Components
components = [comp.Lens(name='Lens', z=0.85),
              comp.AstigmaticLens(name='Astigmatic Lens', z=0.7),
              comp.Quadrupole(name='Quadrupole', z=0.63),
              comp.DoubleDeflector(name='Double Deflector', z_up=0.5, z_low=0.45),
              comp.Deflector(name='Single Deflector', z=0.3, defx=0, defy=0),
              comp.Biprism(name='Biprism', z=0.2, theta = np.pi/2, deflection = 0.2),
              comp.Aperture(name='Aperture', z=0.10, aperture_radius_inner=0.05)]

#Generate TEM Model
model_ = Model(components, beam_z=1, beam_type='x_axial',
                   num_rays=32, beam_semi_angle=0.15)

#Save Figure with Matplotlib
fig, ax = show_matplotlib(model_, name = 'all_components.svg', label_fontsize = 18)
fig.savefig('all_components.svg', dpi = 500)
