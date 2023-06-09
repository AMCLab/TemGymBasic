from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import show_matplotlib


components = [comp.Lens(name = 'Condenser Lens', z = 1.2, f = -0.1),
              comp.DoubleDeflector(name = 'Double Deflector', z_up = 0.9, z_low = 0.8, updefx = 1, lowdefx = -1),
              comp.Lens(name = 'Objective Lens', z = 0.6, f = -0.1),
              comp.Sample(name = 'Sample', z = 0.5),
              comp.Lens(name = 'Intermediate Lens', z = 0.4, f = -0.075),
              comp.Lens(name = 'Projector Lens', z = 0.1, f = -0.1)]

axis_view = 'x_axial'
model_ = Model(components, beam_z=1.5, beam_type='x_axial',
                   num_rays=32, gun_beam_semi_angle=0.15)

name = 'beam_tilt.svg'
fig, ax = show_matplotlib(model_, name = name)
fig.suptitle('Beam Pivot Points', fontsize=32)
fig.savefig(name, dpi = 500)
