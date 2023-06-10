from functools import partial
from temgymbasic.functions import get_image_from_rays, convert_rays_to_line_vertices

import PyQt5
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtWidgets import QDesktopWidget

from PyQt5 import QtCore, QtGui, QtWidgets

import pyqtgraph.opengl as gl
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.dockarea import Dock, DockArea

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

import time
import os


# mpl.rcParams['font.family'] = 'Helvetica'
mpl.rc('axes', titlesize=32, labelsize=28)
pg.setConfigOption('imageAxisOrder', 'row-major')

__version__ = "0.5.9.2"
__author__ = "David Landers"


#Create the UI class
class LinearTEMUi(QMainWindow):
    '''Create the UI Window

    Parameters
    ----------
    QMainWindow : class
        Pyqt5's Main window Class
    '''    
    """LinearTEM's Viewer (GUI)."""

    def __init__(self, model):
        '''Init important parameters

        Parameters
        ----------
        model : class
            Microscope model
        '''        
        """View initializer."""
        super().__init__()
        
        #%%% Define Camera Parameters
        self.initial_camera_params = {'center': PyQt5.QtGui.QVector3D(0.5, 0.5, 0.0),
                                 'fov': 25, 'azimuth': -45.0, 'distance': 10, 'elevation': 25.0, }

        self.x_camera_params = {'center': PyQt5.QtGui.QVector3D(0.0, 0.0, 0.5),
                           'fov': 7e-07, 'azimuth': 90.0, 'distance': 143358760, 'elevation': 0.0}

        self.y_camera_params = {'center': PyQt5.QtGui.QVector3D(0.0, 0.0, 0.5),
                           'fov': 7e-07, 'azimuth': 0, 'distance': 143358760, 'elevation': 0.0}
        
        self.model = model

        # Set some main window's properties
        self.setWindowTitle("LinearTEM")
        self.resize(1920, 1080)
        self.centralWidget = DockArea()
        self.setCentralWidget(self.centralWidget)

        # Create Docks
        self.tem_dock = Dock("3D View")
        self.detector_dock = Dock("Detector", size=(5, 5))
        self.gui_dock = Dock("GUI", size=(10, 3))
        self.table_dock = Dock("Parameter Table", size = (5, 5))


        self.centralWidget.addDock(self.tem_dock, "left")

        self.centralWidget.addDock(self.table_dock, "bottom", self.tem_dock)

        self.centralWidget.addDock(self.gui_dock, "right")
        
        self.centralWidget.addDock(self.detector_dock, "above", self.table_dock)
        
        #create detector
        scale = self.model.detector_size/2
        vertices = np.array([[1, 1, 0], [-1, 1, 0], [-1, -1, 0],
                            [1, -1, 0], [1, 1, 0]]) * scale
        
        self.detector_outline = gl.GLLinePlotItem(pos=vertices, color="w", mode='line_strip')
            
        # Create the display and the buttons
        self.create3DDisplay()
        self.createDetectorDisplay()
        self.createGUI()
        
    def create3DDisplay(self):
        '''Create the 3D Display
        '''        
        # Create the 3D TEM Widnow, and plot the components in 3D
        self.tem_window = gl.GLViewWidget()
        
        #Make an axis and addit to the 3D window. Also set up the ray geometry placeholder
        #and detector outline.
        axis = gl.GLAxisItem()
        self.tem_window.addItem(axis)
        
        pos = np.empty((4, 3))
        size = np.empty((4))
        color = np.empty((4, 4))

        pos[0] = (1,0,0); size[0] = 0.1; color[0] = (1.0, 0.0, 0.0, 0.5) #x
        pos[1] = (0,1,0); size[1] = 0.1; color[1] = (0.0, 1.0, 0.0, 0.5) #y
        pos[2] = (0,0,1); size[2] = 0.1; color[2] = (0.0, 0.0, 1.0, 0.5) #z
        pos[3] = (0.125,0.125,0.5); size[3] = 0.1; color[3] = (1.0, 1.0, 1.0, 0.5) #z
        
        sp1 = gl.GLScatterPlotItem(pos=pos, size=size, color=color, pxMode=False)
        
        self.tem_window.addItem(sp1)
        
        self.tem_window.setBackgroundColor((150, 150, 150, 255))
        self.tem_window.setCameraPosition(distance=5)
        self.ray_geometry = gl.GLLinePlotItem(mode='lines', width=2)
        self.tem_window.addItem(self.ray_geometry)
        self.tem_window.addItem(self.detector_outline)
        self.tem_window.setCameraParams(**self.initial_camera_params)
        
        #Loop through all of the model components, and add their geometry to the TEM window.
        for component in self.model.components:
            for geometry in component.gl_points:
                self.tem_window.addItem(geometry)
                
                if component.type == 'Sample':
                    self.tem_window.addItem(component.sample_image_item)
                
            self.tem_window.addItem(component.label)
        
        #Add the ray geometry GLLinePlotItem to the list of geometries for that window
        self.tem_window.addItem(self.ray_geometry)
        
        #Add the window to the dock
        self.tem_dock.addWidget(self.tem_window)

    def createDetectorDisplay(self):
        '''Create the detector display
        '''        
        #Create the detector window, which shows where rays land at the bottom
        self.detector_window = pg.GraphicsLayoutWidget()
        self.detector_window.setAspectLocked(1.0)
        self.spot_img = pg.ImageItem(border="b")
        v2 = self.detector_window.addViewBox()
        v2.setAspectLocked()
        
        #Invert coordinate system so spot moves up when it should
        v2.invertY()
        v2.addItem(self.spot_img)

        self.detector_dock.addWidget(self.detector_window)

    def createGUI(self):
        '''Create the gui display
        '''        
        #Create the window which houses the GUI
        scroll = QScrollArea()
        scroll.setWidgetResizable(1)
        content = QWidget()
        scroll.setWidget(content)
        self.gui_layout = QVBoxLayout(content)
        
        self.gui_dock.addWidget(scroll, 1, 0)
        
        self.model.create_gui()

        self.gui_layout.addWidget(self.model.gui.box, 0)
        self.gui_layout.addWidget(self.model.experiment_gui.box, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(1)
        content = QWidget()
        scroll.setWidget(content)
        self.table_layout = QVBoxLayout(content)
        
        self.table_dock.addWidget(scroll, 1, 0)
        
        # self.model.create_gui()

        #Loop through all components, and display the GUI for each
        for idx, component in enumerate(self.model.components, start = 1):
            component.create_gui()
            self.gui_layout.addWidget(component.gui.box, idx)
            self.table_layout.addWidget(component.gui.table, 0)
    
# Create a Controller class to connect the GUI and the model
class LinearTEMCtrl:
    '''Control code which links the model and 3D viewer
    '''
    def __init__(self, model, viewer):
        '''

        Parameters
        ----------
        model : class
            Microscope model
        view : class
            UI Viewer
        '''        
        self.model = model
        self.viewer = viewer
        
        self.scan_started = False
        
        #Create a timer for 
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(0)
        
        # Connect signals and slots
        self.connectSignals()
        self.update()
    
    def scantimerstart(self):
        '''Start a timer that will update the scan positions
        '''
        self.timer.start()
        self.scan_started = not self.scan_started
        self.model.scan_pixel_x = 0
        self.model.scan_pixel_y = 0
    
    def wobbletimerstart(self, btn, component):
        '''Start a timer that will update the beam wobblers which is used to set the deflector ratio

        Parameters
        ----------
        btn : PyQt5 Button
            ''
        component : class
            Check which component GUI has clicked the button, so we know what timer to start
        '''        
        # checking if button state is checked
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
        else:
            self.timer.stop()

    def connectSignals(self):
        '''Connect the updates of the model to the GUI
        '''        
        self.model.gui.rayslider.valueChanged.connect(self.update)
        self.model.experiment_gui.scanpixelsslider.valueChanged.connect(self.update)
        self.model.gui.checkBoxParalell.stateChanged.connect(self.update)
        self.model.gui.checkBoxPoint.stateChanged.connect(self.update)
        self.model.gui.checkBoxAxial.stateChanged.connect(self.update)
        self.model.gui.beamangleslider.valueChanged.connect(self.update)
        self.model.gui.beamwidthslider.valueChanged.connect(self.update)
        self.model.gui.init_button.clicked.connect(partial(self.set_camera_params, self.model.gui.init_button))
        self.model.gui.x_button.clicked.connect(partial(self.set_camera_params, self.model.gui.x_button))
        self.model.gui.y_button.clicked.connect(partial(self.set_camera_params, self.model.gui.y_button))
        self.model.gui.xangleslider.valueChanged.connect(self.update)
        self.model.gui.yangleslider.valueChanged.connect(self.update)
        
        if self.model.experiment == '4DSTEM':
            self.model.experiment_gui.FOURDSTEM_experiment_button.clicked.connect(self.scantimerstart)
            
        for component in self.model.components:
            if component.type == 'Lens':
                component.gui.fslider.valueChanged.connect(self.update)
                component.gui.fwobble.toggled.connect(partial(self.wobbletimerstart, component.gui.fwobble, component))
            elif component.type == 'Deflector':
                component.gui.defxslider.valueChanged.connect(self.update)
                component.gui.defyslider.valueChanged.connect(self.update)
            elif component.type == 'Double Deflector':
                component.gui.updefxslider.valueChanged.connect(self.update)
                component.gui.updefyslider.valueChanged.connect(self.update)
                component.gui.lowdefxslider.valueChanged.connect(self.update)
                component.gui.lowdefyslider.valueChanged.connect(self.update)
                component.gui.defratioxslider.valueChanged.connect(self.update)
                component.gui.defratioyslider.valueChanged.connect(self.update)
                component.gui.xbuttonwobble.toggled.connect(partial(self.wobbletimerstart, component.gui.xbuttonwobble, component))
                component.gui.ybuttonwobble.toggled.connect(partial(self.wobbletimerstart, component.gui.ybuttonwobble, component))
            elif component.type == 'Biprism':
                component.gui.defslider.valueChanged.connect(self.update)
                component.gui.rotslider.valueChanged.connect(self.update)
            elif component.type == 'Aperture':
                component.gui.radiusslider.valueChanged.connect(self.update)
                component.gui.xslider.valueChanged.connect(self.update)
                component.gui.yslider.valueChanged.connect(self.update)
            elif component.type == 'Astigmatic Lens':
                component.gui.fxslider.valueChanged.connect(self.update)
                component.gui.fyslider.valueChanged.connect(self.update)
            elif component.type == 'Quadrupole':
                component.gui.fxslider.valueChanged.connect(self.update)
                component.gui.fyslider.valueChanged.connect(self.update)
            elif component.type == 'Sample':
                component.gui.xslider.valueChanged.connect(self.update)
                component.gui.yslider.valueChanged.connect(self.update)
    
    def set_camera_params(self, btn):
        '''

        Parameters
        ----------
        btn : PyQt5 Button
            ''
        '''        
        if btn == self.model.gui.x_button:
            self.viewer.tem_window.setCameraParams(**self.viewer.x_camera_params)
        elif btn == self.model.gui.y_button:
            self.viewer.tem_window.setCameraParams(**self.viewer.y_camera_params)
        elif btn == self.model.gui.init_button:
            self.viewer.tem_window.setCameraParams(**self.viewer.initial_camera_params)
            
            
    def update(self):
        '''Update the model
        '''        
        if self.viewer is not None:
            self.model.update_parameters_from_gui()
            
            if self.timer.isActive() and self.model.experiment == '4DSTEM' and self.scan_started == True:
                self.model.update_scan_position()
                self.model.update_scan_coil_ratio()
                
                if self.model.scan_pixel_y == self.model.scan_pixels & self.model.scan_pixel_x == self.model.scan_pixels:
                    self.timer.stop()
                    self.scan_started = False
            else:
                #update components
                for component in self.model.components:
                    component.update_parameters_from_gui()
            
            self.model.step()
            lines_paired, allowed_rays = convert_rays_to_line_vertices(self.model)
                            
            #Create detector image of rays
            detector_ray_image, detector_sample_image, _ = get_image_from_rays(
                self.model.r[-1, 0, allowed_rays], self.model.r[-1, 2, allowed_rays], 
                self.model.r[self.model.sample_r_idx, 0, allowed_rays], self.model.r[self.model.sample_r_idx, 2, allowed_rays], 
                self.model.detector_size, self.model.detector_pixels,
                self.model.components[self.model.sample_idx].sample_size, self.model.components[self.model.sample_idx].sample_pixels,
                self.model.components[self.model.sample_idx].sample
                )
            
            #Update the spot image and the rays of the viewerer 
            self.viewer.spot_img.setImage(detector_sample_image)
            self.viewer.ray_geometry.setData(pos=lines_paired, color=(0, 0.8, 0, 0.05))
    
class Ui_splashui(object):
    def setupUi(self, splashui):
        splashui.setObjectName("splashui")
        splashui.resize(747, 327)
        splashui.setStyleSheet("")
        self.label = QtWidgets.QLabel(splashui)
        self.label.setGeometry(QtCore.QRect(40, 30, 661, 261))
        self.label.setObjectName("label")

        self.retranslateUi(splashui)
        QtCore.QMetaObject.connectSlotsByName(splashui)

    def retranslateUi(self, splashui):
        _translate = QtCore.QCoreApplication.translate
        splashui.setWindowTitle(_translate("splashui", "Form"))
        self.label.setText(_translate("splashui", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#0089cd;\">TemGym</span><span style=\" font-size:18pt; font-weight:600; color:#009100;\">Basic</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Created By David Landers, Dr. Andy Stewart, Dr. Ian Clancy, </span></p><p align=\"center\"><span style=\" font-size:12pt;\">Dr. Dieter Weber, Prof. Rafal Dunin-Borkowski.</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Automated Microscopy &amp; Crystallography Lab</span></p><p align=\"center\"><span style=\" font-size:12pt;\">DOI - Coming Soon</span></p></body></html>"))

class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
    
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.splash = Ui_splashui()
        self.splash.setupUi(self)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def sleep(self):
        time.sleep(3)

def run_pyqt(model):
    '''Main code to run a pyqt model

    Parameters
    ----------
    model : class
        Microscope Model
    '''    
    #Generate the GUI
    splash = SplashScreen()
    splash.show()
    
    viewer = LinearTEMUi(model)
    
    #Connect the model with the viewer
    LinearTEMCtrl(model, viewer)
    
    splash.sleep()
    splash.close()

    return viewer
    
#Example code to make a matplotlib plot
def show_matplotlib(model, name = 'model.svg', component_lw = 4, edge_lw = 1, label_fontsize = 20):
    '''Code to show a matplotlib model

    Parameters
    ----------
    model : class
        Microscope Model
    name : str, optional
        Name of file, by default 'model.svg'
    component_lw : int, optional
        Linewidth of component outline, by default 4
    edge_lw : int, optional
        Linewidth of highlight to edges, by default 1
    label_fontsize : int, optional
        Fontsize of labels, by default 20

    Returns
    -------
    fig : class
        Matplotlib figure object
    ax : class
        Matplotlib axis object of the figure
    '''    
    #Step the rays through the model to get the ray positions throughout the column
    rays = model.step()

    #Collect their x, y & z coordinates
    x, y, z = rays[:, 0, :], rays[:, 2, :], model.z_positions

    #Create a figure
    fig, ax = plt.subplots(figsize=(12, 20))

    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.tick_params(axis='both', which='minor', labelsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(color='lightgrey', linestyle='--', linewidth=0.5)
    ax.grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    ax.set_yticks([])
    ax.set_yticklabels([])
    
    ax.get_xaxis().set_ticks(
        [-model.detector_size/2, 0, model.detector_size/2])
    ax.set_xlim([-0.5, 0.5])
    ax.set_ylim([0, model.beam_z])
    ax.set_aspect('equal', adjustable='box')
    ax.text(0, model.beam_z, 'Electron Gun', fontsize=label_fontsize, zorder = 1000)
    
    #Set starting index of component so that we can plot rays from one component to the next
    idx = 1

    #Generate a list of the allowed rays, so we can block them when they hit an aperture
    allowed_rays = range(model.num_rays)
    
    #Set colors of rays
    ray_color = 'dimgray'
    fill_color = 'aquamarine'
    fill_color_pair = ['khaki', 'deepskyblue']

    fill_alpha = 1
    ray_alpha = 1

    ray_lw = 0.25

    plot_rays = True
    highlight_edges = True
    fill_between = True

    edge_rays = [0, model.num_rays-1]
    label_x = 0.30
    
    #Loop through components, and for each type of component plot rays in the correct ray,
    #and increment the index correctly
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
                    component.name, fontsize=label_fontsize, zorder = 1000)

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
                    component.name, fontsize=label_fontsize, zorder = 1000)
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
                    component.name, fontsize=label_fontsize, zorder = 1000)
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
                    component.name, fontsize=label_fontsize, zorder = 1000)
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
                    'Lower ' + component.name, fontsize=label_fontsize, zorder = 1000)
            ax.plot([-r, 0], [z[idx], z[idx]],
                    color='lightcoral', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([0, r], [z[idx], z[idx]],
                    color='lightblue', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([-r, r], [z[idx], z[idx]],
                    color='k', alpha=0.8, linewidth=component_lw+2, zorder=998)
            idx += 1

        elif component.type == 'Lens':
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize, zorder = 1000)
            ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                         theta1=0, theta2=180, linewidth=1, fill=False, zorder=-1, edgecolor='k'))
            ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                         theta1=180, theta2=0, linewidth=1, fill=False, zorder=999, edgecolor='k'))

            idx += 1

        elif component.type == 'Astigmatic Lens':
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize, zorder = 1000)
            ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                         theta1=0, theta2=180, linewidth=1, fill=False, zorder=-1, edgecolor='k'))
            ax.add_patch(mpl.patches.Arc((0, component.z), component.radius*2, height=0.05,
                                         theta1=180, theta2=0, linewidth=1, fill=False, zorder=999, edgecolor='k'))

            idx += 1
        elif component.type == 'Deflector':
            r = component.radius
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize, zorder = 1000)
            ax.plot([-r, 0], [z[idx], z[idx]],
                    color='lightcoral', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([0, r], [z[idx], z[idx]],
                    color='lightblue', alpha=1, linewidth=component_lw, zorder=999)
            ax.plot([-r, r], [z[idx], z[idx]],
                    color='k', alpha=0.8, linewidth=component_lw+2, zorder=998)

            idx += 1
        elif component.type == 'Sample':
            ax.text(label_x, component.z-0.01,
                    component.name, fontsize=label_fontsize, zorder = 1000)
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
        
    #We need to repeat the code once more for the rays at the end
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
    
    #Create the final labels and plot the detector shape
    ax.text(label_x, -0.01, 'Detector', fontsize=label_fontsize, zorder = 1000)
    ax.plot([-model.detector_size/2, model.detector_size/2],
            [0, 0], color='dimgrey', alpha=1, linewidth=component_lw)
    
    return fig, ax
