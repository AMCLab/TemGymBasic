
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole
from model import buildmodel
import matplotlib.pyplot as plt

components = [Lens(name = 'Lens', z = 0.5, f = -0.1)]

model = buildmodel(components, beam_z = 1.0, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.15)
rays = model.step()

x, y, z = rays[:, 0, :], rays[:, 2, :], model.z_positions

plt.plot(x, z, color = 'green', linewidth = 0.5, alpha = 0.7)
