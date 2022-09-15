from components import Lens, Aperture
from model import buildmodel
from main import show_matplotlib

components = [Aperture(name = 'Condenser Aperture', z = 0.3, x = 0, y = 0, aperture_radius_inner = 0.075),
              Lens(name = 'Condenser Lens', z = 0.2, f = -0.5)]


model = buildmodel(components, beam_z=1.0, beam_type='x_axial',
                   num_rays=32, beam_semi_angle=0.15)

name = 'condenser_aperture.svg'
fig, ax = show_matplotlib(model, name = name)
fig.suptitle('Condenser Aperture', fontsize=32)
fig.savefig(name, dpi = 500)


