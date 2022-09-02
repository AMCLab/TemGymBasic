
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture, AstigmaticLens, Quadrupole, Sample
from model import buildmodel
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import bisect 

mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rc('axes', titlesize=32, labelsize=28)

components = [Biprism(name = 'Condenser Biprism', z = 0.7, theta=np.pi/2, width = 0.01),
              Sample(name = 'Sample', z = 0.5, width = 0.2, x = -0.1),
              Biprism(name = 'Biprism 1', z = 0.4, theta=np.pi/2, width = 0.01),
              Biprism(name = 'Biprism 2', z = 0.2, theta=np.pi/2, width = 0.01)]

axis_view = 'x_axial'
model = buildmodel(components, beam_z=1.0, beam_type='x_axial',
                   num_rays=32, beam_semi_angle=0.15)
rays = model.step()


x, y, z = rays[:, 0, :], rays[:, 2, :], model.z_positions

label_fontsize = 24

fig, ax = plt.subplots(figsize = (8, 5))

ax.set_ylabel('z axis (a.u)')
ax.tick_params(axis='both', which='major', labelsize=14)
ax.tick_params(axis='both', which='minor', labelsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.grid(color='lightgrey', linestyle='--', linewidth=0.5)
ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
ax.minorticks_on()

ax.get_xaxis().set_ticks([-model.detector_size/2, 0, model.detector_size/2])
ax.set_xlim([-0.5, 0.5])
ax.set_ylim([0, model.beam_z])
ax.set_aspect('equal', adjustable='box')
ax.text(0, model.beam_z, 'Electron Gun', fontsize=label_fontsize)

idx = 1

allowed_rays = range(model.num_rays)

ray_color = 'dimgray'
fill_color = 'aquamarine'
fill_color_pair = ['khaki', 'deepskyblue']

fill_alpha = 1
ray_alpha = 1

ray_lw = 0.25
edge_lw = 1
component_lw = 2

plot_rays = True
highlight_edges = True
fill_between = True

edge_rays = [0, model.num_rays-1]
central_ray = (model.num_rays-1)//2
label_x = 0.30

for component in model.components:
    if allowed_rays != []:
        if highlight_edges == True:
            ax.plot(x[idx-1:idx+1, edge_rays], z[idx-1:idx+1],
                    color='k', linewidth=edge_lw, alpha=1, zorder = 2)
        if fill_between == True:
            pair_idx = 0
            for first, second in zip(edge_rays[::2], edge_rays[1::2]):
                if len(edge_rays) == 4:
                    ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second], color = fill_color_pair[pair_idx], edgecolor = fill_color_pair[pair_idx], alpha = fill_alpha, zorder = 0, lw = None)
                    pair_idx +=1
                else:
                    ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second], color = fill_color, edgecolor = fill_color, alpha = fill_alpha, zorder = 0, lw = None)
        if plot_rays == True:
            ax.plot(x[idx-1:idx+1, allowed_rays], z[idx-1:idx+1],
                    color=ray_color, linewidth=ray_lw, alpha=ray_alpha, zorder = 1)
            
    if component.type == 'Biprism':
        ax.text(label_x, component.z-0.01, component.name, fontsize=label_fontsize)
        
        if axis_view == 'x_axial' and component.theta == 0:
            ax.plot(component.points[0, :], component.points[2,
                    :], color='dimgrey', alpha=0.8, linewidth = component_lw)
        elif axis_view == 'x_axial' and component.theta == np.pi/2:
            ax.add_patch(plt.Circle((0, component.z), component.width,
                         edgecolor='k', facecolor='w', zorder=1000))

        idx += 1
    elif component.type == 'Quadrupole':
        r = component.radius
        ax.text(label_x, component.z-0.01, 'Upper ' +
                component.name, fontsize=label_fontsize)
        ax.plot([-r, -r/2], [z[idx], z[idx]],
                color='lightcoral', alpha=0.8, linewidth = component_lw)
        ax.plot([-r/2, 0], [z[idx], z[idx]],
                color='lightblue', alpha=0.8, linewidth = component_lw)
        ax.plot([0, r/2], [z[idx], z[idx]],
                color='lightcoral', alpha=0.8, linewidth = component_lw)
        ax.plot([r/2, r], [z[idx], z[idx]],
                color='lightblue', alpha=0.8, linewidth = component_lw)

        idx += 1

    elif component.type == 'Aperture':
        ax.text(label_x, component.z-0.01, component.name, fontsize=label_fontsize)
        ri = component.aperture_radius_inner
        ro = component.aperture_radius_outer

        ax.plot([-ri, -ro], [z[idx], z[idx]],
                color='dimgrey', alpha=0.8, linewidth = component_lw)
        ax.plot([ri, ro], [z[idx], z[idx]],
                color='dimgrey', alpha=0.8, linewidth = component_lw)

        idx += 1
    elif component.type == 'Double Deflector':
        r = component.radius
        ax.text(label_x, component.z_up-0.01, 'Upper ' +
                component.name, fontsize=label_fontsize)
        ax.plot([-r, 0], [z[idx], z[idx]],
                color='lightcoral', alpha=0.8, linewidth = component_lw)
        ax.plot([0, r], [z[idx], z[idx]],
                color='lightblue', alpha=0.8, linewidth = component_lw)

        idx += 1
        
        if allowed_rays != []:
            if highlight_edges == True:
                ax.plot(x[idx-1:idx+1, edge_rays], z[idx-1:idx+1],
                        color='k', linewidth=edge_lw, alpha=1, zorder = 2)
            if fill_between == True:
                pair_idx = 0
                for first, second in zip(edge_rays[::2], edge_rays[1::2]):
                    if len(edge_rays) == 4:
                        ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second], color = fill_color_pair[pair_idx], alpha = fill_alpha, zorder = 1)
                        pair_idx +=1
                    else:
                        ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second], color = fill_color, alpha = fill_alpha, zorder = 0)
            if plot_rays == True:
                ax.plot(x[idx-1:idx+1, allowed_rays], z[idx-1:idx+1],
                        color=ray_color, linewidth=ray_lw, alpha=ray_alpha, zorder = 1)

        ax.text(label_x, component.z_low-0.01,
                'Lower ' + component.name, fontsize=label_fontsize)
        ax.plot([-r, 0], [z[idx], z[idx]],
                color='lightcoral', alpha=0.8, linewidth = component_lw)
        ax.plot([0, r], [z[idx], z[idx]],
                color='lightblue', alpha=0.8, linewidth = component_lw)

        idx += 1
    elif component.type == 'Lens':
        ax.text(label_x, component.z-0.01, component.name, fontsize=label_fontsize)
        # ax.plot(component.points[0, :], component.points[2,
        #         :], color='dimgrey', alpha=0.8, linewidth=component_lw)
        # ax.add_patch(mpl.patches.Ellipse((0, component.z), height = 0.05, width = component.radius*2,
        #              edgecolor='k', facecolor='w', zorder=-1))
        ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                     theta1=0, theta2=180, linewidth=1, fill=False, zorder=-1, edgecolor = 'k'))
        ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                     theta1=180, theta2=0, linewidth=1, fill=False, zorder=999, edgecolor = 'k'))


        idx += 1
    
    elif component.type == 'Sample':
        ax.text(label_x, component.z-0.01, component.name, fontsize=label_fontsize)
        w = component.width
        ax.plot([component.x-w/2, component.x+w/2], [z[idx], z[idx]],
                color='dimgrey', alpha=0.8, linewidth = 3)
        
        idx += 1
            
    allowed_rays = list(set(allowed_rays).difference(
        set(component.blocked_ray_idcs)))
    
    edge_rays = [allowed_rays[0], allowed_rays[-1]]
    new_edges = np.where(np.diff(allowed_rays) != 1)[0].tolist()
    
    for new_edge in new_edges:
        edge_rays.extend([allowed_rays[new_edge], allowed_rays[new_edge+1]])
    
    edge_rays.sort()
    

if allowed_rays != []:
    if highlight_edges == True:
        ax.plot(x[idx-1:idx+1, edge_rays], z[idx-1:idx+1],
                color='k', linewidth=edge_lw, alpha=1, zorder = 2)
    if fill_between == True:
        pair_idx = 0
        for first, second in zip(edge_rays[::2], edge_rays[1::2]):
            if len(edge_rays) == 4:
                ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second], color = fill_color_pair[pair_idx], edgecolor = fill_color_pair[pair_idx], alpha = fill_alpha, zorder = 1)
                pair_idx +=1
            else:
                ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second], color = fill_color, edgecolor = fill_color, alpha = fill_alpha, zorder = 0)
    if plot_rays == True:
        ax.plot(x[idx-1:idx+1, allowed_rays], z[idx-1:idx+1],
                color=ray_color, linewidth=ray_lw, alpha=ray_alpha, zorder = 1)

ax.text(label_x, -0.01, 'Detector', fontsize=label_fontsize)
ax.plot([-model.detector_size/2, model.detector_size/2],
        [0, 0], color='dimgrey', alpha=1, linewidth = component_lw)

plt.savefig('split_condenser.svg', dpi = 500)





