
from PyQt5.QtWidgets import (
    QSlider,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QCheckBox,
    QPushButton,
    QLineEdit
)

from PyQt5.QtGui import QDoubleValidator, QValidator

import numpy as np
from pyqtgraph.Qt import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from functools import partial

# class NotEmptyValidator(QValidator):

    
    # def validate(self, text: str, pos):
    #     if text.strip().isdigit():
    #         state = QValidator.Acceptable
    #     else:
    #         state = QValidator.Intermediate  # so that field can be made empty temporarily
    #     return state, text, pos
    
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
            self.fslider.setMinimum(-10)
            self.fslider.setMaximum(10)
            self.fslider.setValue(1)
            self.fslider.setTickPosition(QSlider.TicksBelow)
            
            self.flineedit = QLineEdit("{:.4f}".format(f))
            self.flineeditstep = QLineEdit("{:.4f}".format(0.1))
            
            self.fwobblefreqlineedit = QLineEdit("{:.4f}".format(1))
            self.fwobbleamplineedit = QLineEdit("{:.4f}".format(0.5))
            
            qdoublevalidator = QDoubleValidator()
            self.flineedit.setValidator(qdoublevalidator)
            self.flineeditstep.setValidator(qdoublevalidator)
            self.fwobblefreqlineedit.setValidator(qdoublevalidator)
            self.fwobbleamplineedit.setValidator(qdoublevalidator)
            
            self.fwobble = QCheckBox('Wobble Lens Current')

            hbox = QHBoxLayout()
            hbox_lineedit = QHBoxLayout()
            hbox_lineedit.addWidget(QLabel('Focal Length = '))
            hbox_lineedit.addWidget(self.flineedit)
            hbox_lineedit.addWidget(QLabel('Slider Step = '))
            hbox_lineedit.addWidget(self.flineeditstep)
            hbox_slider = QHBoxLayout()
            hbox_slider.addWidget(self.fslider)
            hbox_wobble = QHBoxLayout()
            hbox_wobble.addWidget(self.fwobble)
            hbox_wobble.addWidget(QLabel('Wobble Frequency'))
            hbox_wobble.addWidget(self.fwobblefreqlineedit)
            hbox_wobble.addWidget(QLabel('Wobble Amplitude'))
            hbox_wobble.addWidget(self.fwobbleamplineedit)

            vbox = QVBoxLayout()
            vbox.addLayout(hbox_lineedit)
            vbox.addLayout(hbox_slider)
            vbox.addLayout(hbox_wobble)
            vbox.addStretch()

            self.box.setLayout(vbox)
            
            self.table = QGroupBox(name)
            self.flabel_table = QLabel('Focal Length = ' + "{:.2f}".format(f))
            self.flabel_table.setMinimumWidth(80)
            hbox = QHBoxLayout()
            hbox = QHBoxLayout()
            hbox.addWidget(self.flabel_table)

            vbox = QVBoxLayout()
            vbox.addLayout(hbox)
            self.table.setLayout(vbox)
            
class AstigmaticLensGui():
    '''Gui for the Astigmatic Lens component
    '''    
    def __init__(self, name, gui_label, comp_type, fx, fy):
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
        self.fxslider.setMinimum(-10)
        self.fxslider.setMaximum(10)
        self.fxslider.setValue(1)
        self.fxslider.setTickPosition(QSlider.TicksBelow)
        self.fxlineedit = QLineEdit("{:.4f}".format(fx))
        self.fxlineeditstep = QLineEdit("{:.4f}".format(0.1))
        
        qdoublevalidator = QDoubleValidator()
        self.fxlineedit.setValidator(qdoublevalidator)
        self.fxlineeditstep.setValidator(qdoublevalidator)
        
        hbox = QHBoxLayout()
        hbox_lineedit = QHBoxLayout()
        hbox_lineedit.addWidget(QLabel('Focal Length X = '))
        hbox_lineedit.addWidget(self.fxlineedit)
        hbox_lineedit.addWidget(QLabel('Slider Step X = '))
        hbox_lineedit.addWidget(self.fxlineeditstep)
        hbox_slider = QHBoxLayout()
        hbox_slider.addWidget(self.fxslider)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_lineedit)
        vbox.addLayout(hbox_slider)
        vbox.addStretch()
        
        self.fyslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.fyslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fyslider.setMinimum(-10)
        self.fyslider.setMaximum(10)
        self.fyslider.setValue(1)
        self.fyslider.setTickPosition(QSlider.TicksBelow)
        
        self.fylineedit = QLineEdit("{:.4f}".format(fy))
        self.fylineeditstep = QLineEdit("{:.4f}".format(0.1))
        self.fywobblineedit = QLineEdit("{:.4f}".format(fy))
        self.fwobblefreqlineedit = QLineEdit("{:.4f}".format(1))
        self.fwobbleamplineedit = QLineEdit("{:.4f}".format(0.5))
        
        self.fylineedit.setValidator(qdoublevalidator)
        self.fylineeditstep.setValidator(qdoublevalidator)
        self.fwobbleamplineedit.setValidator(qdoublevalidator)
        self.fwobblefreqlineedit.setValidator(qdoublevalidator)
        
        self.fwobble = QCheckBox('Wobble Lens Current')

        hbox = QHBoxLayout()
        hbox_lineedit = QHBoxLayout()
        hbox_lineedit.addWidget(QLabel('Focal Length Y = '))
        hbox_lineedit.addWidget(self.fylineedit)
        hbox_lineedit.addWidget(QLabel('Slider Step Y = '))
        hbox_lineedit.addWidget(self.fylineeditstep)
        hbox_slider = QHBoxLayout()
        hbox_slider.addWidget(self.fyslider)
        
        vbox.addLayout(hbox_lineedit)
        vbox.addLayout(hbox_slider)
        
        if comp_type == 'Quadrupole':
            pass
        else:
            hbox_wobble = QHBoxLayout()
            hbox_wobble.addWidget(self.fwobble)
            hbox_wobble.addWidget(QLabel('Wobble Frequency'))
            hbox_wobble.addWidget(self.fwobblefreqlineedit)
            hbox_wobble.addWidget(QLabel('Wobble Amplitude'))
            hbox_wobble.addWidget(self.fwobbleamplineedit)
            vbox.addLayout(hbox_wobble)
            
        vbox.addStretch()

        self.box.setLayout(vbox)
        
        self.table = QGroupBox(name)
        
        self.flabelx_table = QLabel('Focal Length X = ' + "{:.2f}".format(fx))
        self.flabelx_table.setMinimumWidth(80)
        hbox = QHBoxLayout()
        hbox.addWidget(self.flabelx_table)
        
        self.flabely_table = QLabel('Focal Length Y = ' + "{:.2f}".format(fy))
        self.flabely_table.setMinimumWidth(80)
        hbox = QHBoxLayout()
        hbox.addWidget(self.flabely_table)

        vbox = QVBoxLayout()
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
        self.defxslider.setMinimum(-10)
        self.defxslider.setMaximum(10)
        self.defxslider.setValue(1)
        self.defxslider.setTickPosition(QSlider.TicksBelow)
        
        qdoublevalidator = QDoubleValidator()
        self.defxlineedit = QLineEdit("{:.4f}".format(defx))
        self.defxlineeditstep = QLineEdit("{:.4f}".format(0.1))
        self.defxlineedit.setValidator(qdoublevalidator)
        self.defxlineeditstep.setValidator(qdoublevalidator)
        
        self.defyslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.defyslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.defyslider.setMinimum(-10)
        self.defyslider.setMaximum(10)
        self.defyslider.setValue(1)
        self.defyslider.setTickPosition(QSlider.TicksBelow)
        self.defylineedit = QLineEdit("{:.4f}".format(defy))
        self.defylineeditstep = QLineEdit("{:.4f}".format(0.1))
        self.defylineedit.setValidator(qdoublevalidator)
        self.defylineeditstep.setValidator(qdoublevalidator)

        hbox = QHBoxLayout()
        hbox_lineedit = QHBoxLayout()
        hbox_lineedit.addWidget(QLabel('X Deflection = '))
        hbox_lineedit.addWidget(self.defxlineedit)
        hbox_lineedit.addWidget(QLabel('Slider Step X = '))
        hbox_lineedit.addWidget(self.defxlineeditstep)
        hbox_lineedit.addWidget(QLabel('Y Deflection = '))
        hbox_lineedit.addWidget(self.defylineedit)
        hbox_lineedit.addWidget(QLabel('Slider Step Y = '))
        hbox_lineedit.addWidget(self.defylineeditstep)
        hbox_slider = QHBoxLayout()
        hbox_slider.addWidget(self.defxslider)
        hbox_slider.addWidget(self.defyslider)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_lineedit)
        vbox.addLayout(hbox_slider)
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
        self.box = QGroupBox(name)
        
        self.updefxslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.updefxslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.updefxslider.setMinimum(-10)
        self.updefxslider.setMaximum(10)
        self.updefxslider.setValue(1)
        self.updefxslider.setTickPosition(QSlider.TicksBelow)
        self.updefxlineedit = QLineEdit("{:.4f}".format(updefx))
        self.updefxlineeditstep = QLineEdit("{:.4f}".format(0.1))
        
        qdoublevalidator = QDoubleValidator()
        self.updefxlineedit.setValidator(qdoublevalidator)
        self.updefxlineeditstep.setValidator(qdoublevalidator)
        
        self.updefyslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.updefyslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.updefyslider.setMinimum(-10)
        self.updefyslider.setMaximum(10)
        self.updefyslider.setValue(1)
        self.updefyslider.setTickPosition(QSlider.TicksBelow)
        self.updefylineedit = QLineEdit("{:.4f}".format(updefy))
        self.updefylineeditstep = QLineEdit("{:.4f}".format(0.1))
        self.updefylineedit.setValidator(qdoublevalidator)
        self.updefylineeditstep.setValidator(qdoublevalidator)
        
        hbox = QHBoxLayout()
        hbox_lineedit = QHBoxLayout()
        hbox_lineedit.addWidget(QLabel('Upper X Deflection = '))
        hbox_lineedit.addWidget(self.updefxlineedit)
        hbox_lineedit.addWidget(QLabel('Slider Step Upper X = '))
        hbox_lineedit.addWidget(self.updefxlineeditstep)
        hbox_lineedit.addWidget(QLabel('Upper Y Deflection = '))
        hbox_lineedit.addWidget(self.updefylineedit)
        hbox_lineedit.addWidget(QLabel('Slider Step Upper Y = '))
        hbox_lineedit.addWidget(self.updefylineeditstep)
        
        hbox_slider = QHBoxLayout()
        hbox_slider.addWidget(self.updefxslider)
        hbox_slider.addWidget(self.updefyslider)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_lineedit)
        vbox.addLayout(hbox_slider)
        vbox.addStretch()
        
        self.lowdefxslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.lowdefxslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.lowdefxslider.setMinimum(-10)
        self.lowdefxslider.setMaximum(10)
        self.lowdefxslider.setValue(1)
        self.lowdefxslider.setTickPosition(QSlider.TicksBelow)
        self.lowdefxlineedit = QLineEdit("{:.4f}".format(lowdefx))
        self.lowdefxlineeditstep = QLineEdit("{:.4f}".format(0.1))
        self.lowdefxlineedit.setValidator(qdoublevalidator)
        self.lowdefxlineeditstep.setValidator(qdoublevalidator)
        
        self.lowdefyslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.lowdefyslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.lowdefyslider.setMinimum(-10)
        self.lowdefyslider.setMaximum(10)
        self.lowdefyslider.setValue(1)
        self.lowdefyslider.setTickPosition(QSlider.TicksBelow)
        self.lowdefylineedit = QLineEdit("{:.4f}".format(lowdefy))
        self.lowdefylineeditstep = QLineEdit("{:.4f}".format(0.1))
        self.lowdefylineedit.setValidator(qdoublevalidator)
        self.lowdefylineeditstep.setValidator(qdoublevalidator)
        
        hbox = QHBoxLayout()
        hbox_lineedit = QHBoxLayout()
        hbox_lineedit.addWidget(QLabel('Lower X Deflection = '))
        hbox_lineedit.addWidget(self.lowdefxlineedit)
        hbox_lineedit.addWidget(QLabel('Slider Step Lower X = '))
        hbox_lineedit.addWidget(self.lowdefxlineeditstep)
        hbox_lineedit.addWidget(QLabel('Lower Y Deflection = '))
        hbox_lineedit.addWidget(self.lowdefylineedit)
        hbox_lineedit.addWidget(QLabel('Slider Step Lower Y = '))
        hbox_lineedit.addWidget(self.lowdefylineeditstep)
        
        hbox_slider = QHBoxLayout()
        hbox_slider.addWidget(self.lowdefxslider)
        hbox_slider.addWidget(self.lowdefyslider)
        
        vbox.addLayout(hbox_lineedit)
        vbox.addLayout(hbox_slider)
        vbox.addStretch()

        self.xbuttonwobble = QCheckBox("Wobble Upper Deflector X")
        self.defxwobblefreqlineedit = QLineEdit("{:.4f}".format(1))
        self.defxwobbleamplineedit = QLineEdit("{:.4f}".format(0.5))
        self.defxratiolabel = QLabel('Deflector X Response Ratio = ')
        self.defxratiolineedit = QLineEdit("{:.4f}".format(0.0))
        self.defxratiolineeditstep = QLineEdit("{:.4f}".format(0.1))
        
        self.defxratiolineedit.setValidator(qdoublevalidator)
        self.defxratiolineeditstep.setValidator(qdoublevalidator)
        
        self.defxratioslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.defxratioslider.setMinimum(-10)
        self.defxratioslider.setMaximum(10)
        self.defxratioslider.setValue(1)
        self.defxratioslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.defxratioslider.setTickPosition(QSlider.TicksBelow)

        hbox = QHBoxLayout()
        hbox.addWidget(self.xbuttonwobble)
        hbox.addWidget(QLabel('Wobble X Frequency'))
        hbox.addWidget(self.defxwobblefreqlineedit)
        hbox.addWidget(QLabel('Wobble X Amplitude'))
        hbox.addWidget(self.defxwobbleamplineedit)
        vbox.addLayout(hbox)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.defxratiolabel)
        hbox.addWidget(self.defxratiolineedit)
        hbox.addWidget(QLabel('Def Ratio X Response Slider Step = '))
        hbox.addWidget(self.defxratiolineeditstep)
        vbox.addLayout(hbox)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.defxratioslider)
        vbox.addLayout(hbox)

        self.ybuttonwobble = QCheckBox("Wobble Upper Deflector Y")
        self.defywobblefreqlineedit = QLineEdit("{:.4f}".format(1))
        self.defywobbleamplineedit = QLineEdit("{:.4f}".format(0.5))
        self.defyratiolabel = QLabel('Deflector Y Response Ratio = ')
        self.defyratiolineedit = QLineEdit("{:.4f}".format(0.0))
        self.defyratiolineeditstep = QLineEdit("{:.4f}".format(0.1))
        self.defyratiolineedit.setValidator(qdoublevalidator)
        self.defyratiolineeditstep.setValidator(qdoublevalidator)
        
        self.defyratioslider = QSlider(QtCore.Qt.Orientation.Horizontal)
        self.defyratioslider.setMinimum(-10)
        self.defyratioslider.setMaximum(10)
        self.defyratioslider.setValue(1)
        self.defyratioslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.defyratioslider.setTickPosition(QSlider.TicksBelow)
        
        self.usedefratio = QCheckBox("Use Def Ratio")
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.ybuttonwobble)
        hbox.addWidget(QLabel('Wobble Y Frequency'))
        hbox.addWidget(self.defywobblefreqlineedit)
        hbox.addWidget(QLabel('Wobble Y Amplitude'))
        hbox.addWidget(self.defywobbleamplineedit)
        vbox.addLayout(hbox)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.defyratiolabel)
        hbox.addWidget(self.defyratiolineedit)
        hbox.addWidget(QLabel('Def Ratio Y Response Slider Step = '))
        hbox.addWidget(self.defyratiolineeditstep)
        vbox.addLayout(hbox)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.defyratioslider)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.usedefratio)
        vbox.addLayout(hbox)
        
        self.box.setLayout(vbox)

        hbox = QHBoxLayout()
        self.table = QGroupBox(name)
        self.updefxlabel_table = QLabel('Upper X Deflection = ' + "{:.2f}".format(updefx))
        self.updefxlabel_table.setMinimumWidth(80)
        self.updefylabel_table = QLabel('Upper Y Deflection = ' + "{:.2f}".format(updefy))
        self.updefylabel_table.setMinimumWidth(80)
        self.lowdefxlabel_table = QLabel('Lower X Deflection = ' + "{:.2f}".format(updefx))
        self.lowdefxlabel_table.setMinimumWidth(80)
        self.lowdefylabel_table = QLabel('Lower Y Deflection = ' + "{:.2f}".format(updefy))
        self.lowdefylabel_table.setMinimumWidth(80)
        self.defyratiolabel_table = QLabel('Y Deflector Ratio = ' + "{:.2f}".format(1))
        self.defxratiolabel_table = QLabel('X Deflector Ratio = ' + "{:.2f}".format(1))
        
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.updefxlabel_table)
        hbox_labels.addWidget(self.updefylabel_table)
        hbox_labels.addWidget(self.lowdefxlabel_table)
        hbox_labels.addWidget(self.lowdefylabel_table)
        hbox_labels.addWidget(self.defxratiolabel_table)
        hbox_labels.addWidget(self.defyratiolabel_table)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_labels)
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
        self.rotlabel_table = QLabel('Rotation (Radians) = ' + "{:.2f}".format(theta))
        
        hbox = QHBoxLayout()
        hbox_labels = QHBoxLayout()
        hbox_labels.addWidget(self.deflabel_table)
        hbox_labels.addWidget(self.rotlabel_table)
        
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
        self.beamwidthslider.setMinimum(-100)
        self.beamwidthslider.setMaximum(99)
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
        self.radiusslider.setMinimum(int(round(1)))
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

