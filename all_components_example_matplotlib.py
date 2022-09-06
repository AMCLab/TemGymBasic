
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole
from model import buildmodel
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from main import show_matplotlib

components = [AstigmaticLens(name='Astigmatic Lens', z=0.9),
              Lens(name='Lens', z=0.8),
              Quadrupole(name='Quadrupole', z=0.7),
              DoubleDeflector(name='Double Deflector', z_up=0.60, z_low=0.5),
              Deflector(name='Single Deflector', z=0.4, defx=0, defy=0),
              Biprism(name='Biprism', z=0.2, theta = np.pi/2),
              Aperture(name='Aperture', z=0.1, aperture_radius_inner=0.05)]

axis_view = 'x_axial'

model = buildmodel(components, beam_z=1, beam_type='x_axial',
                   num_rays=32, beam_semi_angle=0.15)

show_matplotlib(model)

