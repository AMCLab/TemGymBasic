from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import show_matplotlib

components = [
    comp.AstigmaticLens(name='Condenser Lens', z=0.7, fx=-0.4, fy=-0.6),
    comp.Quadrupole(name='Condenser Stigmator', z=0.5)
]

axis_view = 'x_axial'
model_ = Model(components, beam_z=1.0, beam_type='x_axial',
                   num_rays=32, gun_beam_semi_angle=0.15)

name = 'condenser_astigmatism.svg'
fig, ax = show_matplotlib(model_, name = name)
fig.suptitle('Condenser Astigmatism', fontsize=32)
fig.savefig(name, dpi = 500)
