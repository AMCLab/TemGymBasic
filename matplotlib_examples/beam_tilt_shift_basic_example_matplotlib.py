from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import show_matplotlib


#Showing Beam Shift Pivot Point
components = [comp.DoubleDeflector(name='Double Deflector', z_up=0.80, z_low=0.60, updefx=0.4, lowdefx=-0.4),
              comp.Sample(name='Sample', z=0.4),
              comp.Lens(name='Lens', z=0.20, f=-0.2),
              ]

axis_view = 'x_axial'
model_ = Model(components, beam_z=1.0, beam_type='x_axial',
                   num_rays=64, beam_semi_angle=0.0001)

fig, ax = show_matplotlib(model_, name='beam_shift_basic.svg')
fig.suptitle('Beam Shift', fontsize = 40)
fig.savefig('beam_shift_basic.svg')

#Showing Beam Tilt Pivot Point
components = [comp.DoubleDeflector(name='Double Deflector', z_up=0.80, z_low=0.60, updefx=0.4, lowdefx=-0.8),
              comp.Sample(name='Sample', z=0.4),
              comp.Lens(name='Lens', z=0.20, f=-0.2),
              ]

axis_view = 'x_axial'
model_ = Model(components, beam_z=1.0, beam_type='x_axial',
                   num_rays=64, beam_semi_angle=0.0001)

fig,ax = show_matplotlib(model_, name='beam_tilt_basic.svg')
fig.suptitle('Beam Tilt', fontsize = 40)
fig.savefig('beam_tilt_basic.svg')