from functools import partial
import sys
from functions import get_image_from_rays

# Import QApplication and the required widgets from PyQt5.QtWidgets
import PyQt5
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QApplication

import pyqtgraph.opengl as gl
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.dockarea import Dock, DockArea

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rc('axes', titlesize=32, labelsize=28)

__version__ = "0.1"
__author__ = "David Landers"

class LinearTEMUi(QMainWindow):
    """LinearTEM's View (GUI)."""

    def __init__(self, model):
        """View initializer."""
        super().__init__()
        
        #%%% Define Camera Parameters
        self.initial_camera_params = {'center': PyQt5.QtGui.QVector3D(-0.5, -0.5, 0.0),
                                 'fov': 25, 'azimuth': 45.0, 'distance': 10, 'elevation': 25.0, }

        self.x_camera_params = {'center': PyQt5.QtGui.QVector3D(0.0, 0.0, 0.5),
                           'fov': 7e-07, 'azimuth': 90.0, 'distance': 143358760, 'elevation': 0.0}

        self.y_camera_params = {'center': PyQt5.QtGui.QVector3D(0.0, 0.0, 0.5),
                           'fov': 7e-07, 'azimuth': 0, 'distance': 143358760, 'elevation': 0.0}
        
        self._model = model

        # Set some main window's properties
        self.setWindowTitle("LinearTEM")
        self.resize(1920, 1080)
        self._centralWidget = DockArea()
        self.setCentralWidget(self._centralWidget)

        # Create Docks
        self.tem_dock = Dock("3D View")
        self.detector_dock = Dock("Detector", size=(5, 5))
        self.gui_dock = Dock("GUI", size=(10, 3))

        # place d2 at right edge of d1
        self._centralWidget.addDock(self.tem_dock, "left")
        # place d3 at right edge of d2
        self._centralWidget.addDock(self.detector_dock, "right", self.tem_dock)
        # place d4 at bottom edge
        self._centralWidget.addDock(self.gui_dock, "bottom")
        
        #create detector
        scale = self._model.detector_size/2
        vertices = np.array([[1, 1, 0], [-1, 1, 0], [-1, -1, 0],
                            [1, -1, 0], [1, 1, 0]]) * scale
        
        self.detector_outline = gl.GLLinePlotItem(pos=vertices, color="w", mode='line_strip')

        # Create the display and the buttons
        self._create3DDisplay()
        self._createDetectorDisplay()
        self._createGUI()

    def _create3DDisplay(self):
        """Create the display."""
        # Create the display widget

        # %%% Create the first window, and plot the components in 3D
        self.tem_window = gl.GLViewWidget()

        axis = gl.GLAxisItem()
        self.tem_window.addItem(axis)
        self.tem_window.setBackgroundColor((150, 150, 150, 255))
        self.tem_window.setCameraPosition(distance=5)
        self.ray_geometry = gl.GLLinePlotItem(mode='lines', width=2)
        self.tem_window.addItem(self.ray_geometry)
        self.tem_window.addItem(self.detector_outline)
        self.tem_window.setCameraParams(**self.initial_camera_params)
        
        for component in self._model.components:
            for geometry in component.gl_points:
                self.tem_window.addItem(geometry)
                
            self.tem_window.addItem(component.label)
            
        self.tem_window.addItem(self.ray_geometry)
        self.tem_dock.addWidget(self.tem_window)

    def _createDetectorDisplay(self):
        self.detector_window = pg.GraphicsLayoutWidget()
        self.detector_window.setAspectLocked(1.0)
        self.spot_img = pg.ImageItem(border="b")
        v2 = self.detector_window.addViewBox()
        v2.setAspectLocked()
        v2.invertY()
        v2.addItem(self.spot_img)

        self.detector_dock.addWidget(self.detector_window)

    def _createGUI(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(1)
        content = QWidget()
        scroll.setWidget(content)
        self.layout = QVBoxLayout(content)
        
        self.gui_dock.addWidget(scroll, 1, 0)
        
        self._model.create_gui()

        self.layout.addWidget(self._model.gui.box, 0)
        
        for idx, component in enumerate(self._model.components, start = 1):
            component.create_gui()
            self.layout.addWidget(component.gui.box, idx)
    
# Create a Controller class to connect the GUI and the model
class LinearTEMCtrl:
    """LinearTEM's Controller."""

    def __init__(self, model, view):
        """Controller initializer."""
        self._model = model
        self._view = view
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.setInterval(10)
        
        # Connect signals and slots
        self._connectSignals()
        self._update()
    
    def timerstart(self, btn, component):
        # checking if state is checked
        if btn.isChecked() == True:
            if component.type == 'Double Deflector':
                # if first check box is selected
                if btn == component.gui.xbuttonwobble:
                    self.timer.start()
                    # making other check box to uncheck
                    component.gui.ybuttonwobble.setChecked(False)
                    
                # if second check box is selected
                elif btn == component.gui.ybuttonwobble:
                    self.timer.start()
                    # making other check box to uncheck
                    component.gui.xbuttonwobble.setChecked(False)

            elif component.type == 'Lens':
                self.timer.start()
        else:
            self.timer.stop()

    def _connectSignals(self):
        # """Connect signals and gui"""
        self._model.gui.rayslider.valueChanged.connect(self._update)
        self._model.gui.checkBoxParalell.stateChanged.connect(self._update)
        self._model.gui.checkBoxPoint.stateChanged.connect(self._update)
        self._model.gui.checkBoxAxial.stateChanged.connect(self._update)
        self._model.gui.beamangleslider.valueChanged.connect(self._update)
        self._model.gui.beamwidthslider.valueChanged.connect(self._update)
        self._model.gui.init_button.clicked.connect(partial(self.set_camera_params, self._model.gui.init_button))
        self._model.gui.x_button.clicked.connect(partial(self.set_camera_params, self._model.gui.x_button))
        self._model.gui.y_button.clicked.connect(partial(self.set_camera_params, self._model.gui.y_button))
        self._model.gui.xangleslider.valueChanged.connect(self._update)
        self._model.gui.yangleslider.valueChanged.connect(self._update)
        
        for component in self._model.components:
            if component.type == 'Lens':
                component.gui.fslider.valueChanged.connect(self._update)
                component.gui.fwobble.toggled.connect(partial(self.timerstart, component.gui.fwobble, component))
            elif component.type == 'Deflector':
                component.gui.defxslider.valueChanged.connect(self._update)
                component.gui.defyslider.valueChanged.connect(self._update)
            elif component.type == 'Double Deflector':
                component.gui.updefxslider.valueChanged.connect(self._update)
                component.gui.updefyslider.valueChanged.connect(self._update)
                component.gui.lowdefxslider.valueChanged.connect(self._update)
                component.gui.lowdefyslider.valueChanged.connect(self._update)
                component.gui.defratioxslider.valueChanged.connect(self._update)
                component.gui.defratioyslider.valueChanged.connect(self._update)
                component.gui.xbuttonwobble.toggled.connect(partial(self.timerstart, component.gui.xbuttonwobble, component))
                component.gui.ybuttonwobble.toggled.connect(partial(self.timerstart, component.gui.ybuttonwobble, component))
            elif component.type == 'Biprism':
                component.gui.defslider.valueChanged.connect(self._update)
                component.gui.rotslider.valueChanged.connect(self._update)
            elif component.type == 'Aperture':
                component.gui.radiusslider.valueChanged.connect(self._update)
                component.gui.xslider.valueChanged.connect(self._update)
                component.gui.yslider.valueChanged.connect(self._update)
            elif component.type == 'Astigmatic Lens':
                component.gui.fxslider.valueChanged.connect(self._update)
                component.gui.fyslider.valueChanged.connect(self._update)
            elif component.type == 'Quadrupole':
                component.gui.fxslider.valueChanged.connect(self._update)
                component.gui.fyslider.valueChanged.connect(self._update)
            elif component.type == 'Sample':
                component.gui.xslider.valueChanged.connect(self._update)
                component.gui.yslider.valueChanged.connect(self._update)
    
    def set_camera_params(self, btn):
        if btn == self._model.gui.x_button:
            self._view.tem_window.setCameraParams(**self._view.x_camera_params)
        elif btn == self._model.gui.y_button:
            self._view.tem_window.setCameraParams(**self._view.y_camera_params)
        elif btn == self._model.gui.init_button:
            self._view.tem_window.setCameraParams(**self._view.initial_camera_params)
            
    def _update(self):
        
        self._model.update_gui()
        
        #update components
        for component in self._model.components:
            component.update_gui()

        self._model.step()
        
        ray_z = np.tile(self._model.z_positions, [self._model.num_rays, 1, 1]).T
        
        # Stack with the z coordinates
        ray_xyz = np.hstack((self._model.r[:, [0, 2], :], ray_z))
        
        # Repeat vertices so we can create lines. The shape of this array is [Num Steps*2, 3, Num Rays]
        lines_repeated = np.repeat(ray_xyz[:, :, :], repeats=2, axis=0)[1:-1]
        
        allowed_rays = range(self._model.num_rays)
        for component in self._model.components:
            if len(component.blocked_ray_idcs) != 0:
                
                allowed_rays = list(set(allowed_rays).difference(set(component.blocked_ray_idcs)))
                
                idx = component.index*2+2
                #Get the coordinates of all rays which hit the aperture.
                pts_blocked = lines_repeated[idx, :, component.blocked_ray_idcs]
                
                #Do really funky array manipulation to create a copy of all of these points that is the same shape as the vertices of remaining lines
                #after the aperture
                lines_aperture = np.broadcast_to(pts_blocked[...,None], pts_blocked.shape+(lines_repeated.shape[0]-(idx),)).transpose(2, 1, 0)
                
                #Copy the coordinate of all rays that hit the aperture, to all line vertices after this, so we don't visualise them.
                lines_repeated[idx:, :, component.blocked_ray_idcs] = lines_aperture
        
        # Then restack each line so that we end up with a long list of lines, from [Num Steps*2, 3, Num Rays] > [(Num Steps*2-2)*Num rays, 3]
        # see > https://stackoverflow.com/questions/38509196/efficiently-re-stacking-a-numpy-ndarray
        lines_paired = lines_repeated.transpose(2, 0, 1).reshape(
            lines_repeated.shape[0]*self._model.num_rays, 3)

        detector_image, _ = get_image_from_rays(
            self._model.r[-1, 2, allowed_rays], self._model.r[-1, 0, allowed_rays], self._model.detector_size, self._model.detector_pixels)

        self._view.spot_img.setImage(detector_image.T)

        self._view.ray_geometry.setData(pos=lines_paired, color=(0, 0.8, 0, 0.05))

def run_pyqt(model):
    AppWindow = QApplication(sys.argv)
    AppWindow.setStyleSheet("QLabel{font-size: 10pt;}")
    
    viewer = LinearTEMUi(model)
    LinearTEMCtrl(model, viewer)
    viewer.show()
    sys.exit(AppWindow.exec_())
    

def show_matplotlib(model):
    rays = model.step()

    x, y, z = rays[:, 0, :], rays[:, 2, :], model.z_positions

    label_fontsize = 12

    fig, ax = plt.subplots(figsize=(8, 20))

    ax.set_ylabel('z axis (a.u)')
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', labelsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.grid(color='lightgrey', linestyle='--', linewidth=0.5)
    ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    ax.minorticks_on()

    ax.get_xaxis().set_ticks(
        [-model.detector_size/2, 0, model.detector_size/2])
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
    component_lw = 4

    plot_rays = True
    highlight_edges = True
    fill_between = True

    edge_rays = [0, model.num_rays-1]
    label_x = 0.30

    for component in model.components:
        if allowed_rays != []:
            if highlight_edges == True:
                ax.plot(x[idx-1:idx+1, edge_rays], z[idx-1:idx+1],
                        color='k', linewidth=edge_lw, alpha=1, zorder=2)
            if fill_between == True:
                pair_idx = 0
                for first, second in zip(edge_rays[::2], edge_rays[1::2]):
                    if len(edge_rays) == 4:
                        ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second],
                                         color=fill_color_pair[pair_idx], edgecolor=fill_color_pair[pair_idx], alpha=fill_alpha, zorder=0, lw=None)
                        pair_idx += 1
                    else:
                        ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second],
                                         color=fill_color, edgecolor=fill_color, alpha=fill_alpha, zorder=0, lw=None)
            if plot_rays == True:
                ax.plot(x[idx-1:idx+1, allowed_rays], z[idx-1:idx+1],
                        color=ray_color, linewidth=ray_lw, alpha=ray_alpha, zorder=1)

        if component.type == 'Biprism':
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize)

            if model.beam_type == 'x_axial' and component.theta == 0:
                ax.plot(component.points[0, :], component.points[2,
                        :], color='dimgrey', alpha=0.8, linewidth=component_lw)
            elif model.beam_type == 'x_axial' and component.theta == np.pi/2:
                ax.add_patch(plt.Circle((0, component.z), component.width,
                             edgecolor='k', facecolor='w', zorder=1000))

            idx += 1
        elif component.type == 'Quadrupole':
            r = component.radius
            ax.text(label_x, component.z-0.01, 'Upper ' +
                    component.name, fontsize=label_fontsize)
            ax.plot([-r, -r/2], [z[idx], z[idx]],
                    color='lightcoral', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([-r/2, 0], [z[idx], z[idx]],
                    color='lightblue', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([0, r/2], [z[idx], z[idx]],
                    color='lightcoral', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([r/2, r], [z[idx], z[idx]],
                    color='lightblue', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([-r, r], [z[idx], z[idx]],
                    color='k', alpha=0.8, linewidth=component_lw+2, zorder=998)
            idx += 1

        elif component.type == 'Aperture':
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize)
            ri = component.aperture_radius_inner
            ro = component.aperture_radius_outer

            ax.plot([-ri, -ro], [z[idx], z[idx]],
                    color='dimgrey', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([ri, ro], [z[idx], z[idx]],
                    color='dimgrey', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([-ri, -ro], [z[idx], z[idx]],
                    color='k', alpha=1, linewidth=component_lw+2, zorder=998)
            ax.plot([ri, ro], [z[idx], z[idx]],
                    color='k', alpha=1, linewidth=component_lw+2, zorder=998)

            idx += 1
        elif component.type == 'Double Deflector':
            r = component.radius
            ax.text(label_x, component.z_up-0.01, 'Upper ' +
                    component.name, fontsize=label_fontsize)
            ax.plot([-r, 0], [z[idx], z[idx]],
                    color='lightcoral', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([0, r], [z[idx], z[idx]],
                    color='lightblue', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([-r, r], [z[idx], z[idx]],
                    color='k', alpha=0.8, linewidth=component_lw+2, zorder=998)
            idx += 1

            if allowed_rays != []:
                if highlight_edges == True:
                    ax.plot(x[idx-1:idx+1, edge_rays], z[idx-1:idx+1],
                            color='k', linewidth=edge_lw, alpha=1, zorder=2)
                if fill_between == True:
                    pair_idx = 0
                    for first, second in zip(edge_rays[::2], edge_rays[1::2]):
                        if len(edge_rays) == 4:
                            ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1,
                                             second], color=fill_color_pair[pair_idx], alpha=fill_alpha, zorder=1)
                            pair_idx += 1
                        else:
                            ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx -
                                             1:idx+1, second], color=fill_color, alpha=fill_alpha, zorder=0)
                if plot_rays == True:
                    ax.plot(x[idx-1:idx+1, allowed_rays], z[idx-1:idx+1],
                            color=ray_color, linewidth=ray_lw, alpha=ray_alpha, zorder=1)

            ax.text(label_x, component.z_low-0.01,
                    'Lower ' + component.name, fontsize=label_fontsize)
            ax.plot([-r, 0], [z[idx], z[idx]],
                    color='lightcoral', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([0, r], [z[idx], z[idx]],
                    color='lightblue', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([-r, r], [z[idx], z[idx]],
                    color='k', alpha=0.8, linewidth=component_lw+2, zorder=998)
            idx += 1

        elif component.type == 'Lens':
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize)
            ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                         theta1=0, theta2=180, linewidth=1, fill=False, zorder=-1, edgecolor='k'))
            ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                         theta1=180, theta2=0, linewidth=1, fill=False, zorder=999, edgecolor='k'))

            idx += 1

        elif component.type == 'Astigmatic Lens':
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize)
            ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                         theta1=0, theta2=180, linewidth=1, fill=False, zorder=-1, edgecolor='k'))
            ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                         theta1=180, theta2=0, linewidth=1, fill=False, zorder=999, edgecolor='k'))

            idx += 1
        elif component.type == 'Deflector':
            r = component.radius
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize)
            ax.plot([-r, 0], [z[idx], z[idx]],
                    color='lightcoral', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([0, r], [z[idx], z[idx]],
                    color='lightblue', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([-r, r], [z[idx], z[idx]],
                    color='k', alpha=0.8, linewidth=component_lw+2, zorder=998)

            idx += 1
        elif component.type == 'Sample':
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize)
            w = component.width
            ax.plot([component.x-w/2, component.x+w/2], [z[idx], z[idx]],
                    color='dimgrey', alpha=0.8, linewidth=3)

            idx += 1

        allowed_rays = list(set(allowed_rays).difference(
            set(component.blocked_ray_idcs)))
        allowed_rays.sort()

        if len(allowed_rays) > 0:
            edge_rays = [allowed_rays[0], allowed_rays[-1]]
            new_edges = np.where(np.diff(allowed_rays) != 1)[0].tolist()

            for new_edge in new_edges:
                edge_rays.extend(
                    [allowed_rays[new_edge], allowed_rays[new_edge+1]])

            edge_rays.sort()

        else:
            break

    if allowed_rays != []:
        if highlight_edges == True:
            ax.plot(x[idx-1:idx+1, edge_rays], z[idx-1:idx+1],
                    color='k', linewidth=edge_lw, alpha=1, zorder=2)
        if fill_between == True:
            pair_idx = 0
            for first, second in zip(edge_rays[::2], edge_rays[1::2]):
                if len(edge_rays) == 4:
                    ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second],
                                     color=fill_color_pair[pair_idx], edgecolor=fill_color_pair[pair_idx], alpha=fill_alpha, zorder=1)
                    pair_idx += 1
                else:
                    ax.fill_betweenx(z[idx-1:idx+1], x[idx-1:idx+1, first], x[idx-1:idx+1, second],
                                     color=fill_color, edgecolor=fill_color, alpha=fill_alpha, zorder=0)
        if plot_rays == True:
            ax.plot(x[idx-1:idx+1, allowed_rays], z[idx-1:idx+1],
                    color=ray_color, linewidth=ray_lw, alpha=ray_alpha, zorder=1)

    ax.text(label_x, -0.01, 'Detector', fontsize=label_fontsize)
    ax.plot([-model.detector_size/2, model.detector_size/2],
            [0, 0], color='dimgrey', alpha=1, linewidth=component_lw)

    plt.savefig('model_tem.svg', dpi=500)

    return fig, ax
