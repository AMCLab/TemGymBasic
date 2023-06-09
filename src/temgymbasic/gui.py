
from PyQt5.QtWidgets import (
    QSlider,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QCheckBox,
    QPushButton
)

import numpy as np
from pyqtgraph.Qt import QtCore
from functools import partial

'''This code makes the GUI interface for each component. 
There is a lot of copypaste in this section'''

class LensGui():

        def __init__(self, name, f):
            '''GUI for the Lens component
            ----------
            name : str
                Name of component
            f : float
                Focal length
            '''
            self.box = QGroupBox(name)
            self.fslider = QSlider(QtCore.Qt.Orientation.Horizontal)
            self.fslider.setTickPosition(QSlider.TickPosition.TicksBelow)
            self.fslider.setMinimum(-1000)
            self.fslider.setMaximum(-10)
            self.fslider.setValue(int(round(f*1000)))
            self.fslider.setTickPosition(QSlider.TicksBelow)

            self.flabel = QLabel('Focal Length = ' + "{:.2f}".format(f))
            self.flabel.setMinimumWidth(80)
            self.fwobble = QCheckBox('Wobble Lens Current')

            hbox = QHBoxLayout()
            hbox_labels = QHBoxLayout()
            hbox_labels.addWidget(self.flabel)
            hbox.addSpacing(10)
            hbox.addWidget(self.fslider)
            hbox.addSpacing(5)
            hbox.addWidget(self.fwobble)

            vbox = QVBoxLayout()
            vbox.addLayout(hbox_labels)
            vbox.addLayout(hbox)
            vbox.addStretch()

            self.box.setLayout(vbox)
            
            self.table = QGroupBox(name)
            self.flabel_table = QLabel('Focal Length = ' + "{:.2f}".format(f))
            self.flabel_table.setMinimumWidth(80)
            hbox = QHBoxLayout()
            hbox_labels = QHBoxLayout()
            hbox_labels.addWidget(self.flabel_table)

            vbox = QVBoxLayout()
            vbox.addLayout(hbox_labels)
            vbox.addLayout(hbox)
            self.table.setLayout(vbox)
            
class AstigmaticLensGui():
    '''Gui for the Astigmatic Lens component
    '''    
    def __init__(self, name, gui_label, fx, fy):
        '''

        Parameters
        ----------
        name : str
            Name of component
        gui_label : str
            Label of focal length slider in GUI
        fx : float
            Focal length in x axis
        fy : float
            Focal length in y axis
        '''
        self.box = QGroupBox(name)
        self.fxslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.fxslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fxslider.setMinimum(-3000)
        self.fxslider.setMaximum(-10)
        self.fxslider.setValue(int(round(fx*1000)))
        self.fxslider.setTickPosition(QSlider.TicksBelow)

        self.fxlabel = QLabel(gui_label + 'X = ' + "{:.2f}".format(fx))
        self.fxlabel.setMinimumWidth(80)

        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.fxlabel)
        hbox.addSpacing(10)
        hbox.addWidget(self.fxslider)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        self.fyslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.fyslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fyslider.setMinimum(-3000)
        self.fyslider.setMaximum(-10)
        self.fyslider.setValue(int(round(fy*1000)))
        self.fyslider.setTickPosition(QSlider.TicksBelow)

        self.fylabel = QLabel(gui_label + 'Y = ' + "{:.2f}".format(fy))
        self.fylabel.setMinimumWidth(80)

        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.fylabel)
        hbox.addSpacing(10)
        hbox.addWidget(self.fyslider)

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        vbox.addStretch()

        self.box.setLayout(vbox)
        
        self.table = QGroupBox(name)
        self.fxlabel_table = QLabel(gui_label + 'X = ' + "{:.2f}".format(fy))
        self.fxlabel_table.setMinimumWidth(80)
        self.fylabel_table = QLabel(gui_label + 'Y = ' + "{:.2f}".format(fy))
        self.fylabel_table.setMinimumWidth(80)
        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.fxlabel_table)
        hbox_labels.addWidget(self.fylabel_table)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        self.table.setLayout(vbox)


class SampleGui():
    '''Gui to allow a user to move the sample in the 3D model
    '''    
    def __init__(self, name, x, y):
        '''

        Parameters
        ----------
        name : str
            Name of the component
        x : float
            X position of component
        y : float
            Y position of component
        '''
        self.box = QGroupBox(name)
        self.xslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.xslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.xslider.setMinimum(-100)
        self.xslider.setMaximum(100)
        self.xslider.setValue(int(round(x)))
        self.xslider.setTickPosition(QSlider.TicksBelow)

        self.xlabel = QLabel('X Position = ' + "{:.2f}".format(x))
        self.xlabel.setMinimumWidth(80)

        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.xlabel)
        hbox.addSpacing(10)
        hbox.addWidget(self.xslider)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        self.yslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.yslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.yslider.setMinimum(-100)
        self.yslider.setMaximum(100)
        self.yslider.setValue(int(round(y)))
        self.yslider.setTickPosition(QSlider.TicksBelow)

        self.ylabel = QLabel('Y Position = ' + "{:.2f}".format(y))
        self.ylabel.setMinimumWidth(80)

        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.ylabel)
        hbox.addSpacing(10)
        hbox.addWidget(self.yslider)

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        vbox.addStretch()

        self.box.setLayout(vbox)
        
        self.table = QGroupBox(name)
        self.xlabel_table = QLabel('X Position = ' + "{:.2f}".format(x))
        self.xlabel_table.setMinimumWidth(80)
        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.xlabel_table)
        
        self.ylabel_table = QLabel('Y Position = ' + "{:.2f}".format(y))
        self.ylabel_table.setMinimumWidth(80)
        hbox_labels.addWidget(self.ylabel_table)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        self.table.setLayout(vbox)

class DeflectorGui():
    '''GUI for the deflector component
    '''    
    def __init__(self, name, defx, defy):
        '''

        Parameters
        ----------
        name : str
            Name of component
        defx : float
            Initial X deflection of deflector
        defy : float
            Initial Y deflection of deflector
        '''
        self.box = QGroupBox(name)
        self.defxslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.defxslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.defxslider.setMinimum(-3000)
        self.defxslider.setMaximum(3000)
        self.defxslider.setValue(int(round(defx*1000)))
        self.defxslider.setTickPosition(QSlider.TicksBelow)

        self.defxlabel = QLabel('X Deflection = ' + "{:.2f}".format(defx))
        self.defxlabel.setMinimumWidth(80)

        self.defyslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.defyslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.defyslider.setMinimum(-3000)
        self.defyslider.setMaximum(3000)
        self.defyslider.setValue(int(round(defx*1000)))
        self.defyslider.setTickPosition(QSlider.TicksBelow)

        self.defylabel = QLabel('Y Deflection = ' + "{:.2f}".format(defy))
        self.defylabel.setMinimumWidth(80)

        vbox = QVBoxLayout()
        self.def_slider_label = QLabel('Deflector Sliders')
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.def_slider_label)
        hbox_labels.addStretch()

        hbox = QHBoxLayout()
        hbox.addWidget(self.defxslider)
        hbox.addSpacing(10)
        hbox.addWidget(self.defxlabel)
        hbox.addSpacing(10)
        hbox.addWidget(self.defyslider)
        hbox.addSpacing(10)
        hbox.addWidget(self.defylabel)

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        vbox.addStretch()

        self.box.setLayout(vbox)
        
        self.table = QGroupBox(name)
        self.defxlabel_table = QLabel('X Deflection = ' + "{:.2f}".format(defx))
        self.defxlabel_table.setMinimumWidth(80)
        self.defylabel_table = QLabel('Y Deflection = ' + "{:.2f}".format(defy))
        self.defylabel_table.setMinimumWidth(80)
        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.defxlabel_table)
        hbox_labels.addWidget(self.defylabel_table)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        self.table.setLayout(vbox)


class DoubleDeflectorGui():
    '''GUI for the double deflector component
    '''    
    def __init__(self, name, updefx, updefy, lowdefx, lowdefy):
        '''

        Parameters
        ----------
        name : str
            Name of component
        updefx : float
            Initial X deflection of upper deflector
        updefy : float
            Initial Y deflection of upper deflector
        lowdefx : float
            Initial X deflection of lower deflector
        lowdefy : float
            Initial Y deflection of lower deflector
        '''        
        self.button_wobble = QCheckBox("Wobble Upper Deflector")
        self.box = QGroupBox(name)
        self.updefxslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.updefxslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.updefxslider.setMinimum(-3000)
        self.updefxslider.setMaximum(3000)
        self.updefxslider.setValue(int(round(updefx*1000)))
        self.updefxslider.setTickPosition(QSlider.TicksBelow)

        self.updefxlabel = QLabel('X Deflection = ' + "{:.2f}".format(updefx))
        self.updefxlabel .setMinimumWidth(80)

        self.updefyslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.updefyslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.updefyslider.setMinimum(-3000)
        self.updefyslider.setMaximum(3000)
        self.updefyslider.setValue(int(round(updefx*1000)))
        self.updefyslider.setTickPosition(QSlider.TicksBelow)

        self.updefylabel = QLabel('Y Deflection = ' + "{:.2f}".format(updefy))
        self.updefylabel .setMinimumWidth(80)

        vbox = QVBoxLayout()
        self.def_slider_label = QLabel('Upper Deflector Sliders')
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.def_slider_label)
        hbox_labels.addStretch()

        hbox = QHBoxLayout()
        hbox.addWidget(self.updefxslider)
        hbox.addSpacing(10)
        hbox.addWidget(self.updefxlabel)
        hbox.addSpacing(10)
        hbox.addWidget(self.updefyslider)
        hbox.addSpacing(10)
        hbox.addWidget(self.updefylabel)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        vbox.addSpacing(20)

        self.lowdefxslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.lowdefxslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.lowdefxslider.setMinimum(-3000)
        self.lowdefxslider.setMaximum(3000)
        self.lowdefxslider.setValue(int(round(lowdefx*1000)))
        self.lowdefxslider.setTickPosition(QSlider.TicksBelow)

        self.lowdefxlabel = QLabel('X Deflection = ' + "{:.2f}".format(lowdefx))
        self.lowdefxlabel.setMinimumWidth(80)

        self.lowdefyslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.lowdefyslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.lowdefyslider.setMinimum(-4000)
        self.lowdefyslider.setMaximum(4000)
        self.lowdefyslider.setValue(int(round(lowdefx*1000)))
        self.lowdefyslider.setTickPosition(QSlider.TicksBelow)

        self.lowdefylabel = QLabel('Y Deflection = ' + "{:.2f}".format(lowdefy))
        self.lowdefylabel .setMinimumWidth(80)

        self.def_slider_label = QLabel('Lower Deflector Sliders')
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.def_slider_label)
        hbox_labels.addStretch()

        hbox = QHBoxLayout()
        hbox.addWidget(self.lowdefxslider)
        hbox.addSpacing(10)
        hbox.addWidget(self.lowdefxlabel)
        hbox.addSpacing(10)
        hbox.addWidget(self.lowdefyslider)
        hbox.addSpacing(10)
        hbox.addWidget(self.lowdefylabel)

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        vbox.addSpacing(20)

        self.xbuttonwobble = QCheckBox("Wobble Upper Deflector X")
        self.defratioxlabel = QLabel('Deflector X Response Ratio = ' + "{:.2f}".format(0))
        self.defratioxslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.defratioxslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.defratioxslider.setMinimum(-4000)
        self.defratioxslider.setMaximum(4000)
        self.defratioxslider.setValue(-1000)
        self.defratioxslider.setTickPosition(QSlider.TicksBelow)

        hbox = QHBoxLayout()
        hbox.addWidget(self.xbuttonwobble)
        hbox.addSpacing(10)
        hbox.addWidget(self.defratioxslider)
        hbox.addSpacing(10)
        hbox.addWidget(self.defratioxlabel)

        vbox.addLayout(hbox)

        self.ybuttonwobble = QCheckBox("Wobble Upper Deflector Y")
        self.defratioylabel = QLabel(
            'Deflector Y Response Ratio = ' + "{:.2f}".format(0))
        self.defratioyslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.defratioyslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.defratioyslider.setMinimum(-3000)
        self.defratioyslider.setMaximum(3000)
        self.defratioyslider.setValue(-1000)
        self.defratioyslider.setTickPosition(QSlider.TicksBelow)

        hbox = QHBoxLayout()
        hbox.addWidget(self.ybuttonwobble)
        hbox.addSpacing(10)
        hbox.addWidget(self.defratioyslider)
        hbox.addSpacing(10)
        hbox.addWidget(self.defratioylabel)

        vbox.addLayout(hbox)
        vbox.addStretch()
        
        self.usedefratio = QCheckBox("Use Def Ratio to Deflect Lower Deflector")
        hbox = QHBoxLayout()
        hbox.addWidget(self.usedefratio)

        vbox.addLayout(hbox)
        vbox.addStretch()

        self.box.setLayout(vbox)
        
        self.table = QGroupBox(name)
        self.defratioxlabel_table = QLabel('Deflector X Response Ratio = ' + "{:.2f}".format(0))
        self.defratioylabel_table = QLabel('Deflector Y Response Ratio = ' + "{:.2f}".format(0))
        self.lowdefxlabel_table = QLabel('X Deflection = ' + "{:.2f}".format(lowdefx))
        self.lowdefylabel_table = QLabel('Y Deflection = ' + "{:.2f}".format(lowdefy))
        self.updefxlabel_table = QLabel('X Deflection = ' + "{:.2f}".format(updefx))
        self.updefylabel_table = QLabel('Y Deflection = ' + "{:.2f}".format(updefy))
        
        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.updefxlabel_table)
        hbox_labels.addWidget(self.updefylabel_table)
        hbox_labels.addWidget(self.lowdefxlabel_table)
        hbox_labels.addWidget(self.lowdefylabel_table)
        hbox_labels.addWidget(self.defratioxlabel_table)
        hbox_labels.addWidget(self.defratioylabel_table)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        self.table.setLayout(vbox)


class BiprismGui():
    '''GUI for the biprism component
    '''    
    def __init__(self, name, deflection, theta):
        '''

        Parameters
        ----------
        name : str
            Name of component
        deflection : float
            Deflection angle in Slope units
        theta : int
            Angle of biprism. Determines if the biprism creates deflects in the x or y direction.
            Two options: 0 or 1. 0 for 0 degrees, 1 for 90 degree rotation. 

        '''
        self.box = QGroupBox(name)
        self.defslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.defslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.defslider.setMinimum(-2000)
        self.defslider.setMaximum(2000)
        self.defslider.setValue(int(round(deflection*1000)))
        self.defslider.setTickPosition(QSlider.TicksBelow)

        self.deflabel = QLabel('Biprism Deflection = ' + "{:.2f}".format(deflection))
        self.deflabel.setMinimumWidth(80)

        vbox = QVBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.deflabel)

        hbox = QHBoxLayout()
        hbox.addWidget(self.defslider)

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        self.rotslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.rotslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.rotslider.setMinimum(0)
        self.rotslider.setMaximum(1)
        self.rotslider.setValue(theta)
        self.rotslider.setTickPosition(QSlider.TicksBelow)

        self.rotlabel = QLabel('Rotation (Radians) = ' + "{:.2f}".format(theta))
        self.rotlabel.setMinimumWidth(80)

        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.rotlabel)

        hbox = QHBoxLayout()
        hbox.addWidget(self.rotslider)

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        vbox.addStretch()

        self.box.setLayout(vbox)
        
        self.table = QGroupBox(name)
        self.deflabel_table = QLabel('Biprism Deflection = ' + "{:.2f}".format(deflection))
        
        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.updefxlabel_table)
        hbox_labels.addWidget(self.updefylabel_table)
        hbox_labels.addWidget(self.lowdefxlabel_table)
        hbox_labels.addWidget(self.lowdefylabel_table)
        hbox_labels.addWidget(self.defratioylabel_table)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        self.table.setLayout(vbox)

# 
class ModelGui():
    '''Overall GUI of the model
    '''    
    def __init__(self, num_rays, beam_type, gun_beam_semi_angle, beam_tilt_x, beam_tilt_y, beam_radius):
        '''

        Parameters
        ----------
        num_rays : int
            Number of rays in the model
        beam_type : str
            Type of initial beam: Axial, paralell of point. 
        gun_beam_semi_angle : float
            Semi angle of the beam 
        beam_tilt_x : float
            Initial x tilt of the beam in radians
        beam_tilt_y : float
            Initial y tilt of the beam in radians
        '''
        self.box = QGroupBox('Model Settings')
        self.rayslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.rayslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.rayslider.setMinimum(4)
        self.rayslider.setMaximum(15)
        self.rayslider.setValue(int(np.log2(num_rays)))
        self.rayslider.setTickPosition(QSlider.TicksBelow)

        self.raylabel = QLabel(str(num_rays))
        self.raylabel.setMinimumWidth(80)
        self.modelraylabel = QLabel('Number of Rays')

        vbox = QVBoxLayout()
        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.addWidget(self.rayslider)
        hbox.addSpacing(15)
        hbox.addWidget(self.raylabel)

        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.modelraylabel)
        hbox_labels.addStretch()

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        self.beamangleslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.beamangleslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.beamangleslider.setMinimum(0)
        self.beamangleslider.setMaximum(157)
        self.beamangleslider.setValue(int(round(gun_beam_semi_angle, 2)*100))
        self.beamangleslider.setTickPosition(QSlider.TicksBelow)

        self.beamanglelabel = QLabel(str(round(gun_beam_semi_angle, 2)))
        self.beamanglelabel.setMinimumWidth(80)
        self.modelbeamanglelabel = QLabel('Axial/Paralell Beam Semi Angle')

        hbox = QHBoxLayout()
        hbox.addWidget(self.beamangleslider)
        hbox.addSpacing(15)
        hbox.addWidget(self.beamanglelabel)
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.modelbeamanglelabel)
        hbox_labels.addStretch()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        self.beamwidthslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.beamwidthslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.beamwidthslider.setMinimum(0)
        self.beamwidthslider.setMaximum(1000)
        self.beamwidthslider.setValue(1)
        self.beamwidthslider.setTickPosition(QSlider.TicksBelow)

        self.beamwidthlabel = QLabel('0')
        self.beamwidthlabel.setMinimumWidth(80)
        self.modelbeamwidthlabel = QLabel('Paralell Beam Width')

        hbox = QHBoxLayout()
        hbox.addWidget(self.beamwidthslider)
        hbox.addSpacing(15)
        hbox.addWidget(self.beamwidthlabel)
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.modelbeamwidthlabel)
        hbox_labels.addStretch()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        self.checkBoxAxial = QCheckBox("Axial Beam")

        self.checkBoxPoint = QCheckBox("Point Beam")

        self.checkBoxParalell = QCheckBox("Paralell Beam")

        self.checkBoxParalell.stateChanged.connect(
            partial(self.uncheck, self.checkBoxParalell))
        self.checkBoxPoint.stateChanged.connect(
            partial(self.uncheck, self.checkBoxPoint))
        self.checkBoxAxial.stateChanged.connect(
            partial(self.uncheck, self.checkBoxAxial))

        hbox.addWidget(self.checkBoxAxial)
        hbox.addWidget(self.checkBoxPoint)
        hbox.addWidget(self.checkBoxParalell)

        if beam_type == 'axial':
            self.checkBoxAxial.setChecked(True)
        elif beam_type == 'paralell':
            self.checkBoxParalell.setChecked(True)
        elif beam_type == 'point':
            self.checkBoxPoint.setChecked(True)

        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        self.anglelabel = QLabel('Beam Tilt Offset')
        hbox_labels.addWidget(self.anglelabel)

        self.xanglelabel = QLabel(
            'Beam Tilt X (Radians) = ' + "{:.3f}".format(beam_tilt_x))
        self.xangleslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.xangleslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.xangleslider.setMinimum(-200)
        self.xangleslider.setMaximum(200)
        self.xangleslider.setValue(0)
        self.xangleslider.setTickPosition(QSlider.TicksBelow)

        self.yanglelabel = QLabel(
            'Beam Tilt Y (Radians) = ' + "{:.3f}".format(beam_tilt_y))
        self.yangleslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.yangleslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.yangleslider.setMinimum(-200)
        self.yangleslider.setMaximum(200)
        self.yangleslider.setValue(0)
        self.yangleslider.setTickPosition(QSlider.TicksBelow)

        hbox.addWidget(self.xangleslider)
        hbox.addWidget(self.xanglelabel)

        hbox.addWidget(self.yangleslider)
        hbox.addWidget(self.yanglelabel)

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        self.view_label = QLabel('Set Camera View')
        self.init_button = QPushButton('Initial View')
        self.x_button = QPushButton('X View')
        self.y_button = QPushButton('Y View')

        hbox_label = QHBoxLayout()
        hbox_label.addWidget(self.view_label)
        hbox_push_buttons = QHBoxLayout()
        hbox_push_buttons.addWidget(self.init_button)
        hbox_push_buttons.addSpacing(15)
        hbox_push_buttons.addWidget(self.x_button)
        hbox_push_buttons.addSpacing(15)
        hbox_push_buttons.addWidget(self.y_button)

        vbox.addLayout(hbox_label)
        vbox.addLayout(hbox_push_buttons)

        self.box.setLayout(vbox)

    def uncheck(self, btn):
        '''Determines which button is checked, and unchecks others

        Parameters
        ----------
        btn : Pyqt5 Button
        '''
        # checking if state is checked
        if btn.isChecked() == True:

            # if first check box is selected
            if btn == self.checkBoxAxial:

                # making other check box to uncheck
                self.checkBoxParalell.setChecked(False)
                self.checkBoxPoint.setChecked(False)

            # if second check box is selected
            elif btn == self.checkBoxParalell:

                # making other check box to uncheck
                self.checkBoxAxial.setChecked(False)
                self.checkBoxPoint.setChecked(False)

            # if third check box is selected
            elif btn == self.checkBoxPoint:

                # making other check box to uncheck
                self.checkBoxAxial.setChecked(False)
                self.checkBoxParalell.setChecked(False)


class ApertureGui():
    '''GUI for the aperture component
    '''    
    def __init__(self, name, min_radius, max_radius, inner_radius, x, y):
        '''

        Parameters
        ----------
        name : str
            Name of component
        min_radius : float
            Minimum radius of the aperture
        max_radius : float
            Max radius of the aperture
        inner_radius : float
            Initial inner radius of the aperture
        x : float
            X position of component
        y : float
            y position of component
        '''
        self.box = QGroupBox(name)
        self.radiusslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.radiusslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.radiusslider.setMinimum(int(round(0)))
        self.radiusslider.setMaximum(int(round(max_radius*1000)))
        self.radiusslider.setValue(int(round(inner_radius*1000)))
        self.radiusslider.setTickPosition(QSlider.TicksBelow)

        self.radiuslabel = QLabel('Aperture Radius = ' +
                                  "{:.2f}".format(inner_radius))
        self.radiuslabel.setMinimumWidth(80)

        vbox = QVBoxLayout()
        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.addWidget(self.radiusslider)

        hbox_label = QHBoxLayout()
        hbox_label.addWidget(self.radiuslabel)

        vbox.addLayout(hbox_label)
        vbox.addLayout(hbox)

        self.xslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.xslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.xslider.setMinimum(-100)
        self.xslider.setMaximum(100)
        self.xslider.setValue(int(round(x*1e2)))
        self.xslider.setTickPosition(QSlider.TicksBelow)

        self.xlabel = QLabel('X Position = ' + "{:.2f}".format(x))
        self.xlabel.setMinimumWidth(80)

        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.xlabel)
        hbox.addSpacing(10)
        hbox.addWidget(self.xslider)

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        self.yslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.yslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.yslider.setMinimum(-100)
        self.yslider.setMaximum(100)
        self.yslider.setValue(int(round(y*1e2)))
        self.yslider.setTickPosition(QSlider.TicksBelow)

        self.ylabel = QLabel('Y Position = ' + "{:.2f}".format(y))
        self.ylabel.setMinimumWidth(80)

        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.ylabel)
        hbox.addSpacing(10)
        hbox.addWidget(self.yslider)

        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)

        vbox.addStretch()

        self.box.setLayout(vbox)
        
        self.table = QGroupBox(name)
        self.radiuslabel_table = QLabel('Aperture Radius = ' + "{:.2f}".format(inner_radius))
        self.xlabel_table = QLabel('X Position = ' + "{:.2f}".format(x))
        self.ylabel_table = QLabel('Y Position = ' + "{:.2f}".format(y))
        
        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.xlabel_table)
        hbox_labels.addWidget(self.ylabel_table)
        hbox_labels.addWidget(self.radiuslabel_table)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
        vbox.addLayout(hbox)
        self.table.setLayout(vbox)
        
class ExperimentGui():
    '''GUI for the aperture component
    '''    
    def __init__(self):
        '''

        Parameters
        ----------
        name : str
            Name of component
        min_radius : float
            Minimum radius of the aperture
        max_radius : float
            Max radius of the aperture
        inner_radius : float
            Initial inner radius of the aperture
        x : float
            X position of component
        y : float
            y position of component
        '''
        self.box = QGroupBox('Experiment')
        self.scanpixelsslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.scanpixelsslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.scanpixelsslider.setMinimum(2)
        self.scanpixelsslider.setMaximum(8)
        self.scanpixelsslider.setValue(256)
        
        self.scanpixelslabel = QLabel('Scan pixels = ' + str(int(self.scanpixelsslider.value())))
        self.scanpixelslabel.setMinimumWidth(80)
        
        self.overfocuslabel = QLabel('Overfocus = Not Set')
        self.overfocuslabel.setMinimumWidth(80)
        
        self.cameralengthlabel = QLabel('Camera length = Not Set')
        self.cameralengthlabel.setMinimumWidth(80)
        
        self.semiconvlabel = QLabel('Semi conv = Not Set')
        self.semiconvlabel.setMinimumWidth(80)
        
        self.scanpixelsizelabel = QLabel('Scan pixel size = Not Set')
        self.scanpixelsizelabel.setMinimumWidth(80)

        vbox = QVBoxLayout()
        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.addWidget(self.scanpixelsslider)
        hbox.addSpacing(15)
        hbox.addWidget(self.scanpixelslabel)
        hbox.addSpacing(15)
        hbox.addWidget(self.overfocuslabel)
        hbox.addSpacing(15)
        hbox.addWidget(self.semiconvlabel)
        hbox.addSpacing(15)
        hbox.addWidget(self.scanpixelsizelabel)
        hbox.addSpacing(15)
        hbox.addWidget(self.cameralengthlabel)
        
        
        vbox.addLayout(hbox)
        
        self.FOURDSTEM_experiment_button = QPushButton('Run 4D STEM Experiment')
        
        hbox_push_buttons = QHBoxLayout()
        hbox_push_buttons.addWidget(self.FOURDSTEM_experiment_button)
        vbox.addLayout(hbox_push_buttons)

        self.box.setLayout(vbox)

