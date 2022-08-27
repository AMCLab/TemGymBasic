#!/usr/bin/env python3

# Filename: pycalc.py

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""PyCalc is a simple calculator built using Python and PyQt5."""

import sys
from functools import partial

from functions import get_image_from_rays

# Import QApplication and the required widgets from PyQt5.QtWidgets
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QScrollArea

import pyqtgraph.opengl as gl
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.dockarea import Dock, DockArea

import numpy as np

__version__ = "0.1"
__author__ = "David Landers"

ERROR_MSG = "ERROR"

# Create a subclass of QMainWindow to setup the calculator's GUI


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
        self.layout.addWidget(self._model.gui.box, 0)
        
        for idx, component in enumerate(self._model.components, start = 1):
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

    def _connectSignals(self):
        # """Connect signals and gui"""
        self._model.gui.rayslider.valueChanged.connect(self._update)
        self._model.gui.checkBoxParalell.stateChanged.connect(self._update)
        self._model.gui.checkBoxPoint.stateChanged.connect(self._update)
        self._model.gui.checkBoxAxial.stateChanged.connect(self._update)
        self._model.gui.beamangleslider.valueChanged.connect(self._update)
        self._model.gui.beamwidthslider.valueChanged.connect(self._update)
        
        for component in self._model.components:
            if component.type == 'Lens':
                component.gui.fslider.valueChanged.connect(self._update)
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

