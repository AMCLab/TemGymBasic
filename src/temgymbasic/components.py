import temgymbasic.shapes as geom
from temgymbasic.gui import *
import pyqtgraph.opengl as gl
import numpy as np
from PyQt5.QtGui import QFont
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg

font = QFont()
font.setPixelSize(20)

    
class Lens():
    '''Creates a lens component and handles calls to GUI creation, updates to GUI
        and stores the component matrix.
    '''    
    def __init__(self, z, name = '', f = 0.5, label_radius = 0.3, radius = 0.25, num_points = 50):
        '''

        Parameters
        ----------
        z : float
            Position of component in optic axis
        name : str, optional
            Name of this component which will be displayed by GUI, by default ''
        f : float, optional, 
            Focal length of this lens, by default 0.5
        label_radius : float, optional
            Location to place the label in the 3D GUI, by default 0.3
        radius : float, optional
            Radius of the 3D model of this component, by default 0.25
        num_points : int, optional
            Number of points to use to make the 3D model, by default 50
        '''        
        self.type = 'Lens'
        
        self.z = z
        self.radius = radius 
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.f = f
        self.f_temp = f
        self.ftime = 0
        self.blocked_ray_idcs = []
        
        self.name = name
        self.set_matrix()
        self.set_gl_geom()
        self.set_gl_label()
        
    def lens_matrix(self, f):
        '''Lens ray transfer matrix

        Parameters
        ----------
        f : float
            Focal length of lens

        Returns
        -------
        ndarray
            Output Ray Transfer Matrix
        '''        
        
        matrix = np.array([[1, 0,      0, 0, 0],
                           [-1 / f, 1,      0, 0, 0],
                           [0, 0,      1, 0, 0],
                           [0, 0, -1 / f, 1, 0],
                           [0, 0,       0, 0, 1]])

        return matrix
    
    def set_matrix(self): 

        '''
        '''        
        self.matrix = self.lens_matrix(self.f)
    
    def set_gl_geom(self):
        '''
        '''        
        self.gl_points = []
        self.points = geom.lens(self.radius, self.z, self.num_points)
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.points.T, color="white", width=5))
    
    def set_gl_label(self):
        '''
        '''        
        self.label = gl.GLTextItem(pos=np.array(
            [-self.label_radius, self.label_radius, self.z]), text=self.name, color='w')
        self.label.setData(font = font)
        
    def set_flabel(self):
        '''
        '''        
        self.gui.flabel_table.setText(
            'Focal Length = ' + "{:.2f}".format(float(self.f)))
        
    def create_gui(self):
        '''
        '''        
        self.gui = LensGui(self.name, self.f)
        
        self.gui.flineedit.editingFinished.connect(self.updated_line_edit)
        self.gui.fslider.valueChanged.connect(self.updated_slider)
        
        # self.gui.flineedit.textChanged.connect(partial(self.update_parameters_from_gui, 'QLineEdit'))

    def updated_slider(self, value):
        self.f = self.f_temp + self.gui.fslider.value()*float(self.gui.flineeditstep.text())
        self.gui.flineedit.setText(str(self.f))
        
    def updated_line_edit(self):
        self.f = float(self.gui.flineedit.text())
        self.f_temp = float(self.gui.flineedit.text())
        self.gui.fslider.setValue(1)
        
    def update_parameters_from_gui(self):
     
        '''Update method called by the main loop of the programme
        '''      
        if self.gui.fwobble.isChecked():
            f0 = float(self.gui.flineedit.text())
            self.f = f0 + float(self.gui.fwobbleamplineedit.text())*np.sin(2*np.pi*float(self.gui.fwobblefreqlineedit.text())*self.ftime)
            self.ftime += 1
            
        if abs(self.f) > 1e-14:
            self.set_flabel()
            self.set_matrix()
            

class AstigmaticLens():
    '''Creates an Astigmatic lens component and handles calls to GUI creation, updates to GUI
        and stores the component matrix.
    '''    
    def __init__(self, z, name = '', fx = -0.5, fy = -0.5, label_radius = 0.3, radius = 0.25, num_points = 50):
        '''

        Parameters
        ----------
        z : float
            Position of component in optic axis
        name : str, optional
            Name of this component which will be displayed by GUI, by default ''
        fx : float, optional, 
            Focal length of this lens in x, by default -0.5
        fx : float, optional, 
            Focal length of this lens in y, by default -0.5
        label_radius : float, optional
            Location to place the label in the 3D GUI, by default 0.3
        radius : float, optional
            Radius of the 3D model of this component, by default 0.25
        num_points : int, optional
            Number of points to use to make the 3D model, by default 50
        '''        

        self.type = 'Astigmatic Lens'
        self.gui_label = 'Focal Length '
        self.z = z
        self.radius = radius 
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.fx = fx
        self.fx_temp = fx
        self.fy = fy
        self.fy_temp = fy
        self.ftime = 0

        self.blocked_ray_idcs = []
        
        self.name = name
        
        self.set_gl_geom()
        self.set_gl_label()
        self.set_matrix()
        
    def lens_matrix(self, fx, fy):
        '''Astigmatic lens ray transfer matrix

        Parameters
        ----------
        fx : float
            focal length in x
        fy : float
            focal length in y

        Returns
        -------
        ndarray
            Output Ray Transfer Matrix
        '''        
        
        matrix = np.array([[1, 0,      0, 0, 0],
                           [-1 / fx, 1,      0, 0, 0],
                           [0, 0,      1, 0, 0],
                           [0, 0, -1 / fy, 1, 0],
                           [0, 0,       0, 0, 1]])

        return matrix
    
    def set_matrix(self):
        '''
        '''        
        self.matrix = self.lens_matrix(self.fx, self.fy)
    
    def set_gl_geom(self):
        '''
        '''        
        self.gl_points = []
        self.points = geom.lens(self.radius, self.z, self.num_points)
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.points.T, color="white", width=5))
    
    def set_gl_label(self):
        '''
        '''        
        self.label = gl.GLTextItem(pos=np.array(
            [-self.label_radius, self.label_radius, self.z]), text=self.name, color='w')
        self.label.setData(font = font)
    
    def create_gui(self):
        '''
        '''        
        self.gui = AstigmaticLensGui(self.name, self.gui_label, self.type, self.fx, self.fy)
        
        self.gui.fxlineedit.editingFinished.connect(self.updated_fxline_edit)
        self.gui.fylineedit.editingFinished.connect(self.updated_fyline_edit)
        self.gui.fxslider.valueChanged.connect(self.updated_fxslider)
        self.gui.fyslider.valueChanged.connect(self.updated_fyslider)
            
    def updated_fxslider(self, value):
        self.fx = self.fx_temp + self.gui.fxslider.value()*float(self.gui.fxlineeditstep.text())
        self.gui.fxlineedit.setText(str(self.fx))
        
    def updated_fyslider(self, value):
        self.fy = self.fy_temp + self.gui.fyslider.value()*float(self.gui.fylineeditstep.text())
        self.gui.fylineedit.setText(str(self.fy))
        
    def updated_fxline_edit(self):
        self.fx = float(self.gui.fxlineedit.text())
        self.fx_temp = float(self.gui.fxlineedit.text())
        self.gui.fxslider.setValue(1)
        
    def updated_fyline_edit(self):
        self.fy = float(self.gui.fylineedit.text())
        self.fy_temp = float(self.gui.fylineedit.text())
        self.gui.fyslider.setValue(1)
        
    def update_parameters_from_gui(self):
     
        '''Update method called by the main loop of the programme
        '''      
        
        if self.gui.fwobbleamplineedit.text() == '':
            self.gui.fwobbleamplineedit.setText("0.")
            
        if self.gui.fwobbleamplineedit.text() == '':
            self.gui.fwobbleamplineedit.setText("0.")
            
        if self.gui.fxlineeditstep.text() == '':
            self.gui.fxlineeditstep.setText("0.")
            
        if self.gui.fylineeditstep.text() == '':
            self.gui.fylineeditstep.setText("0.")
            
        if self.gui.fwobble.isChecked():
            f0x = float(self.gui.fxlineedit.text())
            f0y = float(self.gui.fylineedit.text())
            
            self.fx = f0x + float(self.gui.fwobbleamplineedit.text())*np.sin(2*np.pi*float(self.gui.fwobblefreqlineedit.text())*self.ftime)
            self.fy = f0y + float(self.gui.fwobbleamplineedit.text())*np.sin(2*np.pi*float(self.gui.fwobblefreqlineedit.text())*self.ftime)
            self.ftime += 1
            
        if abs(self.fx) > 1e-14 and abs(self.fy) > 1e-14:
            self.set_matrix()
            
class Quadrupole():
    '''Creates a quadrupole component and handles calls to GUI creation, updates to GUI
        and stores the component matrix. Almost exactly the same as astigmatic lens component
        '''
    def __init__(self, z, name = '', fx = -0.5, fy = -0.5, label_radius = 0.3, radius = 0.25, num_points = 50):
        '''

        Parameters
        ----------
        z : float
            Position of component in optic axis
        name : str, optional
            Name of this component which will be displayed by GUI, by default ''
        fx : float, optional, 
            Focal length of this lens in x, by default -0.5
        fx : float, optional, 
            Focal length of this lens in y, by default -0.5
        label_radius : float, optional
            Location to place the label in the 3D GUI, by default 0.3
        radius : float, optional
            Radius of the 3D model of this component, by default 0.25
        num_points : int, optional
            Number of points to use to make the 3D model, by default 50
        '''        

        self.type = 'Quadrupole'
        self.gui_label = 'Stigmator Strength'
        self.z = z
        self.radius = radius 
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.fx = fx
        self.fx_temp = fx
        self.fy = fy
        self.fy_temp = fy
        self.ftime = 0

        self.blocked_ray_idcs = []
        
        self.name = name
        
        self.set_gl_geom()
        self.set_gl_label()
        self.set_matrix()
        
    def lens_matrix(self, fx, fy):
        '''Quadrupole lens ray transfer matrix

        Parameters
        ----------
        fx : float
            focal length in x
        fy : float
            focal length in y

        Returns
        -------
        ndarray
            Output Ray Transfer Matrix
        '''        
        
        matrix = np.array([[1, 0,      0, 0, 0],
                           [-1 / fx, 1,      0, 0, 0],
                           [0, 0,      1, 0, 0],
                           [0, 0, -1 / fy, 1, 0],
                           [0, 0,       0, 0, 1]])

        return matrix
    
    def set_matrix(self):
        '''
        '''        
        self.matrix = self.lens_matrix(self.fx, self.fy)
    
    def set_gl_geom(self):
        '''
        '''        
        self.gl_points = []
        self.points = geom.quadrupole(self.radius, np.pi/6, self.z, self.num_points)

        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.points[0].T, color="b", width=5))
        
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.points[1].T, color="b", width=5))

        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.points[2].T, color="r", width=5))
        
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.points[3].T, color="r", width=5))
    
    
    def set_gl_label(self):
        '''
        '''        
        self.label = gl.GLTextItem(pos=np.array(
            [-self.label_radius, self.label_radius, self.z]), text=self.name, color='w')
        self.label.setData(font = font)
    
    def create_gui(self):
        '''
        '''        
        self.gui = AstigmaticLensGui(self.name, self.gui_label, self.type, self.fx, self.fy)
        
        self.gui.fxlineedit.editingFinished.connect(self.updated_fxline_edit)
        self.gui.fylineedit.editingFinished.connect(self.updated_fyline_edit)
        self.gui.fxslider.valueChanged.connect(self.updated_fxslider)
        self.gui.fyslider.valueChanged.connect(self.updated_fyslider)
            
    def updated_fxslider(self, value):
        self.fx = self.fx_temp + self.gui.fxslider.value()*float(self.gui.fxlineeditstep.text())
        self.gui.fxlineedit.setText(str(self.fx))
        
    def updated_fyslider(self, value):
        self.fy = self.fy_temp + self.gui.fyslider.value()*float(self.gui.fylineeditstep.text())
        self.gui.fylineedit.setText(str(self.fy))
        
    def updated_fxline_edit(self):
        self.fx = float(self.gui.fxlineedit.text())
        self.fx_temp = float(self.gui.fxlineedit.text())
        self.gui.fxslider.setValue(1)
        
    def updated_fyline_edit(self):
        self.fy = float(self.gui.fylineedit.text())
        self.fy_temp = float(self.gui.fylineedit.text())
        self.gui.fyslider.setValue(1)
        
    def update_parameters_from_gui(self):
     
        '''Update method called by the main loop of the programme
        '''      
    
        if self.gui.fxlineeditstep.text() == '':
            self.gui.fxlineeditstep.setText("0.")
            
        if self.gui.fylineeditstep.text() == '':
            self.gui.fylineeditstep.setText("0.")
            
        if abs(self.fx) > 1e-14 and abs(self.fy) > 1e-14:
            self.set_matrix()

class Sample():
    '''Creates a sample component which serves only as a visualisation on the 3D model. 
    '''    
    def __init__(self, z = 0., sample = None, name = '', label_radius = 0.3, width = 0.25, num_points = 50, x = 0., y = 0.):
        '''

        Parameters
        ----------
        z : float
            Position of component in optic axis
        name : str, optional
            Name of this component which will be displayed by GUI, by default ''
        label_radius : float, optional
            Location to place the label in the 3D GUI, by default 0.3
        radius : float, optional
            Radius of the 3D model of this component, by default 0.25
        num_points : int, optional
            Number of points to use to make the 3D model, by default 50
        x : float, optional
            X position of sample model, by default 0.
        y : float, optional
            Y position of sample model, by default 0.
        width : float, optional
            Width of the edges of the square sample, by default 0.25
        '''        

        self.type = 'Sample'
        
        self.x = x
        self.y = y
        self.z = z
        self.width = width 
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.sample_image_x = x - width/2
        self.sample_image_y = y - width/2
        self.sample_image_z = 0

        self.sample = sample
        self.sample_pixels = sample.shape[0]
        self.sample_size = width
        
        self.blocked_ray_idcs = []
        self.name = name
        self.set_matrix()
        self.set_gl_geom()
        self.set_gl_label()

        if sample is not None:
            self.set_gl_image()


    def sample_matrix(self):
        '''Sample transfer matrix - simply a unit matrix of ones because we don't interact with the sample yet. 

        Returns
        -------
        ndarray
            unit matrix
        '''        
        matrix = np.array([[1, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1]])

        return matrix
        
    def set_matrix(self):
        '''
        '''        
        self.matrix = self.sample_matrix()
    
    def set_gl_geom(self):   
        '''
        '''        
        self.gl_points = []
        self.verts = geom.square(self.width, self.x, self.y, self.z)
        
        self.colors = np.ones((self.verts.shape[0], 3, 4))
        self.colors[:, :, 3] = 0.25
        
        self.gl_points.append(gl.GLMeshItem(vertexes=self.verts, vertexColors=self.colors,
                                 smooth=True, drawEdges=False))
        
        self.gl_points[0].setGLOptions('additive')

    def set_gl_image(self):

        tex = pg.makeRGBA(np.abs(self.sample.T), levels = (0, 1))[0]
        self.sample_image_item = gl.GLImageItem(tex)
        self.sample_image_item.scale(self.width/self.sample.shape[0], self.width/self.sample.shape[1], 1)

        
        dx = self.sample_image_x - self.x
        dy = self.sample_image_y - self.y
        self.sample_image_item.translate(dx, dy, 0, local = False)
        self.sample_image_item.rotate(180, 0, 1, 0, local = False)
        
        dz = self.z - self.sample_image_z
        self.sample_image_item.translate(0, 0, dz, local = False)
        self.sample_image_item.rotate(180, 0, 0, 1+dz, local = False)
        
    def create_gui(self): 
        '''
        '''         
        self.gui = SampleGui(self.name, self.x, self.y)

    def set_gl_label(self): 
        '''
        '''        
        self.label = gl.GLTextItem(pos=np.array(
            [-self.label_radius, self.label_radius, self.z]), text=self.name, color='w')
        self.label.setData(font = font)
        
    def set_slabel(self):
        '''
        '''        
        self.gui.xlabel.setText(
            'X = ' + "{:.2f}".format(self.x))
        self.gui.ylabel.setText(
            'Y = ' + "{:.2f}".format(self.y))
        self.gui.xlabel_table.setText(
            'X = ' + "{:.2f}".format(self.x))
        self.gui.ylabel_table.setText(
            'Y = ' + "{:.2f}".format(self.y))
    
    def update_image(self):
        dx = self.x_new-self.x
        dy = self.y_new-self.y
        
        self.sample_image_item.translate(dx, dy, 0, local = False)
        
        self.sample_image_x = self.x + self.width/2
        self.sample_image_y = self.y + self.width/2
    
    def update_mesh(self):
        '''
        '''        
        self.verts = geom.square(self.width, self.x, self.y, self.z)
        
        self.gl_points[0].setMeshData(vertexes=self.verts, vertexColors=self.colors,
                                 smooth=True, drawEdges=False)
    
    def update_parameters_from_gui(self):
        '''
        '''        
        self.x_new = self.gui.xslider.value()*1e-2
        self.y_new = self.gui.yslider.value()*1e-2
        self.update_image()
        
        self.x = self.x_new
        self.y = self.y_new
        self.update_mesh()
        
        self.set_slabel()

class Deflector():
    '''Creates a single deflector component and handles calls to GUI creation, updates to GUI
        and stores the component matrix. See Double Deflector component for a more useful version
    '''    
    def __init__(self, z, name = '', defx = 0.5, defy = 0.5, label_radius = 0.3, radius = 0.25, num_points = 50):
        '''_summary_

        Parameters
        ----------
        z : float
            Position of component in optic axis
        name : str, optional
            Name of this component which will be displayed by GUI, by default ''
        defx : float, optional
            deflection kick in slope units to the incoming ray x angle, by default 0.5
        defy : float, optional
            deflection kick in slope units to the incoming ray y angle, by default 0.5
        label_radius : float, optional
            Location to place the label in the 3D GUI, by default 0.3
        radius : float, optional
            Radius of the 3D model of this component, by default 0.25
        num_points : int, optional
            Number of points to use to make the 3D model, by default 50
        '''         
        self.type = 'Deflector'
        
        self.z = z
        self.radius = radius 
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.defx = defx
        self.defy = defy
        self.defx_temp = defx
        self.defy_temp = defy
        
        self.blocked_ray_idcs = []
        
        self.name = name
        
        self.set_gl_geom()
        self.set_gl_label()
        self.set_matrix()
        
    def deflector_matrix(self, def_x, def_y):
        '''Single deflector ray transfer matrix

        Parameters
        ----------
        def_x : float
            deflection in x in slope units
        def_y : _type_
            deflection in y in slope units

        Returns
        -------
        ndarray
            Output ray transfer matrix
        '''        
        
        matrix = np.array([[1, 0, 0, 0,          0],
                           [0, 1, 0, 0, def_x],
                           [0, 0, 1, 0,          0],
                           [0, 0, 0, 1, def_y],
                           [0, 0, 0, 0,         1]])

        return matrix
    
    def set_matrix(self): 
        '''
        '''        
        self.matrix = self.deflector_matrix(self.defx, self.defy)
    
    def set_gl_geom(self):
        '''
        '''        
        self.gl_points = []
        self.points = geom.deflector(self.radius, np.pi/2, self.z, self.num_points)
        
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.points[0].T, color="r", width=5))
        
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.points[1].T, color="b", width=5))
    
    def set_gl_label(self):  
        '''
        '''        
        self.label = gl.GLTextItem(pos=np.array(
            [-self.label_radius, self.label_radius, self.z]), text=self.name, color='w')
        self.label.setData(font = font)
        
    def set_deflabel(self):
        '''
        '''        
        self.gui.defxlabel_table.setText(
            'X Deflection = ' + "{:.2f}".format(self.defx))
        self.gui.defylabel_table.setText(
            'Y Deflection = ' + "{:.2f}".format(self.defy))
        

    def create_gui(self):  
        '''
        '''        
        self.gui = DeflectorGui(self.name, self.defx, self.defy)
        
        self.gui.defxlineedit.editingFinished.connect(self.updated_defxline_edit)
        self.gui.defylineedit.editingFinished.connect(self.updated_defyline_edit)
        self.gui.defxslider.valueChanged.connect(self.updated_defxslider)
        self.gui.defyslider.valueChanged.connect(self.updated_defyslider)
            
    def updated_defxslider(self, value):
        self.defx = self.defx_temp + self.gui.defxslider.value()*float(self.gui.defxlineeditstep.text())
        self.gui.defxlineedit.setText(str(self.defx))
        
    def updated_defyslider(self, value):
        self.defy = self.defy_temp + self.gui.defyslider.value()*float(self.gui.defylineeditstep.text())
        self.gui.defylineedit.setText(str(self.defy))
        
    def updated_defxline_edit(self):
        self.defx = float(self.gui.defxlineedit.text())
        self.defx_temp = float(self.gui.defxlineedit.text())
        self.gui.defxslider.setValue(1)
        
    def updated_defyline_edit(self):
        self.defy = float(self.gui.defylineedit.text())
        self.defy_temp = float(self.gui.defylineedit.text())
        self.gui.defyslider.setValue(1)
        
    def update_parameters_from_gui(self):
     
        '''Update method called by the main loop of the programme
        '''      
    
        if self.gui.defxlineeditstep.text() == '':
            self.gui.defxlineeditstep.setText("0.")
            
        if self.gui.defylineeditstep.text() == '':
            self.gui.defylineeditstep.setText("0.")
            
        self.set_matrix()
        
    # def update_parameters_from_gui(self):
    #     '''
    #     '''        
    #     self.defx = self.gui.defxslider.value()*1e-3
    #     self.defy = self.gui.defyslider.value()*1e-3
    #     self.set_deflabel()
    #     self.set_matrix()
        
class DoubleDeflector():
    '''Creates a double deflector component and handles calls to GUI creation, updates to GUI
        and stores the component matrix. Primarily used in the Beam Tilt/Shift alignment.
    '''    
    def __init__(self, z_up, z_low, name = '', updefx = 0.0, updefy = 0.0, lowdefx = 0.0, lowdefy = 0.0, 
                 scan_rotation = 0, label_radius = 0.3, radius = 0.25, num_points = 50):
        '''

        Parameters
        ----------
        z_up : float
            Position of the upper deflection component in optic axis
        z_low : float
            Position of the lower deflection component in optic axis
        name : str, optional
            Name of this component which will be displayed by GUI, by default ''
        updefx : float, optional
            deflection kick of upper deflector
            in slope units to the incoming ray x angle,
            by default 0.0
        updefy : float, optional
            deflection kick of upper deflector
            in slope units to the incoming ray y angle,
            by default 0.0
        lowdefx : float, optional
            deflection kick of lower deflector
            in slope units to the incoming ray x angle,
            by default 0.0
        lowdefy : float, optional
            deflection kick of lower deflector
            in slope units to the incoming ray y angle,
            by default 0.0
        label_radius : float, optional
            Location to place the label in the 3D GUI, by default 0.3
        radius : float, optional
            Radius of the 3D model of this component, by default 0.25
        num_points : int, optional
            Number of points to use to make the 3D model, by default 50
        '''        

        self.type = 'Double Deflector'
        
        self.z_up = z_up
        self.z_low = z_low
        self.dist = self.z_up - z_low
        self.radius = radius
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.updefx = updefx
        self.updefy = updefy
        
        self.lowdefx = lowdefx
        self.lowdefy = lowdefy
        
        self.updefx_temp = updefx
        self.updefy_temp = updefy
        
        self.lowdefx_temp = lowdefx
        self.lowdefy_temp = lowdefy
        
        self.defratiox_temp = -1.
        self.defratioy_temp = -1.
        
        self.scan_rotation = scan_rotation
        
        self.defratiox = -1.
        self.defratioy = -1.
        
        self.name = name
        self.blocked_ray_idcs = []
        
        self.set_gl_geom()
        self.set_gl_label()
        self.set_matrices()
        
        self.xtime = 0
        self.ytime = 0
        
    def deflector_matrix(self, def_x, def_y):
        '''Single deflector ray transfer matrix

        Parameters
        ----------
        def_x : float
            deflection in x in slope units
        def_y : _type_
            deflection in y in slope units

        Returns
        -------
        ndarray
            Output ray transfer matrix
        '''        
        matrix = np.array([[1, 0, 0, 0,          0],
                           [0, 1, 0, 0, def_x],
                           [0, 0, 1, 0,          0],
                           [0, 0, 0, 1, def_y],
                           [0, 0, 0, 0,         1]])

        return matrix
    
    def rotation_matrix(self, scan_rotation):
        '''Scan rotation ray transfer matrix

        Parameters
        ----------
        scan_rotation : float
            scan_rotation in degrees

        Returns
        -------
        ndarray
            Output ray transfer matrix
        '''        
        rad = (scan_rotation/180)*np.pi
        matrix = np.array([[np.cos(rad), 0, -np.sin(rad), 0, 0],
                           [0, 1, 0, 0, 0],
                           [np.sin(rad), 0, np.cos(rad), 0, 0],
                           [0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1]])

        return matrix
        
    
    def set_matrices(self):
        '''
        '''        
        self.up_matrix = self.deflector_matrix(self.updefx, self.updefy)
        self.low_matrix = np.matmul(self.rotation_matrix(self.scan_rotation), self.deflector_matrix(self.lowdefx, self.lowdefy))#self.deflector_matrix(self.lowdefx, self.lowdefy)
    
    def set_gl_geom(self):
        '''
        '''        
        self.gl_points = []
        self.uppoints = geom.deflector(self.radius, np.pi/2, self.z_up, self.num_points)
        
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.uppoints[0].T, color="r", width=5))
        
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.uppoints[1].T, color="b", width=5))
        
        self.lowpoints = geom.deflector(self.radius, np.pi/2, self.z_low, self.num_points)
        
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.lowpoints[0].T, color="r", width=5))
        
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.lowpoints[1].T, color="b", width=5))
    
    def set_gl_label(self):
        '''
        '''        
        self.label = gl.GLTextItem(pos=np.array(
            [-self.label_radius, self.label_radius, self.z_up]), text=self.name, color='w')
        self.label.setData(font = font)
        
    def set_deflabel(self): 
        '''
        '''        

        self.gui.updefxlabel_table.setText(
            'X Deflection = ' + "{:.2f}".format(self.updefx))
        self.gui.updefylabel_table.setText(
            'Y Deflection = ' + "{:.2f}".format(self.updefy))
        self.gui.lowdefxlabel_table.setText(
            'X Deflection = ' + "{:.2f}".format(self.lowdefx))
        self.gui.lowdefylabel_table.setText(
            'Y Deflection = ' + "{:.2f}".format(self.lowdefy))
        self.gui.defxratiolabel_table.setText(
            'Lower Deflector X Response Ratio = ' + "{:.2f}".format(self.defratiox))
        self.gui.defyratiolabel_table.setText(
            'Lower Deflector Y Response Ratio = ' + "{:.2f}".format(self.defratioy))
        
    def create_gui(self):
        '''
        '''        
        self.gui = DoubleDeflectorGui(self.name, self.updefx, self.updefy, self.lowdefx, self.lowdefy)
        self.gui.updefxlineedit.editingFinished.connect(self.updated_updefxline_edit)
        self.gui.updefylineedit.editingFinished.connect(self.updated_updefyline_edit)
        self.gui.updefxslider.valueChanged.connect(self.updated_updefxslider)
        self.gui.updefyslider.valueChanged.connect(self.updated_updefyslider)
        
        self.gui.updefxlineeditstep.editingFinished.connect(self.updated_updefxline_editstep)
        self.gui.updefylineeditstep.editingFinished.connect(self.updated_updefyline_editstep)

        self.gui.lowdefxlineedit.editingFinished.connect(self.updated_lowdefxline_edit)
        self.gui.lowdefylineedit.editingFinished.connect(self.updated_lowdefyline_edit)
        self.gui.lowdefxslider.valueChanged.connect(self.updated_lowdefxslider)
        self.gui.lowdefyslider.valueChanged.connect(self.updated_lowdefyslider)
        
        self.gui.lowdefxlineeditstep.editingFinished.connect(self.updated_lowdefxline_editstep)
        self.gui.lowdefylineeditstep.editingFinished.connect(self.updated_lowdefyline_editstep)
        
        self.gui.defxratiolineedit.editingFinished.connect(self.updated_defxratioline_edit)
        self.gui.defyratiolineedit.editingFinished.connect(self.updated_defyratioline_edit)
        self.gui.defxratioslider.valueChanged.connect(self.updated_defxratioslider)
        self.gui.defyratioslider.valueChanged.connect(self.updated_defyratioslider)
        
        self.gui.defxratiolineeditstep.editingFinished.connect(self.updated_defxratioline_editstep)
        self.gui.defyratiolineeditstep.editingFinished.connect(self.updated_defyratioline_editstep)
            
    def updated_updefxslider(self, value):
        self.updefx = self.updefx_temp + self.gui.updefxslider.value()*float(self.gui.updefxlineeditstep.text())
        self.gui.updefxlineedit.setText(str(self.updefx))
        
    def updated_updefyslider(self, value):
        self.updefy = self.updefy_temp + self.gui.updefyslider.value()*float(self.gui.updefylineeditstep.text())
        self.gui.updefylineedit.setText(str(self.updefy))
        
    def updated_updefxline_edit(self):
        self.updefx = float(self.gui.updefxlineedit.text())
        self.updefx_temp = float(self.gui.updefxlineedit.text())
        self.gui.updefxslider.setValue(1)
        
    def updated_updefyline_edit(self):
        self.updefy = float(self.gui.updefylineedit.text())
        self.updefy_temp = float(self.gui.updefylineedit.text())
        self.gui.updefyslider.setValue(1)
        
    def updated_updefxline_editstep(self, value):
        self.gui.updefxslider.setValue(1)
        
    def updated_updefyline_editstep(self, value):
        self.gui.updefyslider.setValue(1)
        
    def updated_lowdefxslider(self, value):
        self.lowdefx = self.lowdefx_temp + self.gui.lowdefxslider.value()*float(self.gui.lowdefxlineeditstep.text())
        self.gui.lowdefxlineedit.setText(str(self.lowdefx))
        
    def updated_lowdefyslider(self, value):
        self.lowdefy = self.lowdefy_temp + self.gui.lowdefyslider.value()*float(self.gui.lowdefylineeditstep.text())
        self.gui.lowdefylineedit.setText(str(self.lowdefy))
        
    def updated_lowdefxline_edit(selfe):
        self.lowdefx = float(self.gui.lowdefxlineedit.text())
        self.lowdefx_temp = float(self.gui.lowdefxlineedit.text())
        self.gui.lowdefxslider.setValue(1)
        
    def updated_lowdefyline_edit(self):
        self.lowdefy = float(self.gui.lowdefylineedit.text())
        self.lowdefy_temp = float(self.gui.lowdefylineedit.text())
        self.gui.lowdefyslider.setValue(1)
        
    def updated_lowdefxline_editstep(self, value):
        self.gui.lowdefxslider.setValue(1)
        
    def updated_lowdefyline_editstep(self, value):
        self.gui.lowdefyslider.setValue(1)
        
    def updated_defxratioslider(self, value):
        self.defratiox = self.defratiox_temp + self.gui.defxratioslider.value()*float(self.gui.defxratiolineeditstep.text())
        self.gui.defxratiolineedit.setText(str(self.defratiox))
        
    def updated_defyratioslider(self, value):
        self.defratioy = self.defratioy_temp + self.gui.defyratioslider.value()*float(self.gui.defyratiolineeditstep.text())
        self.gui.defyratiolineedit.setText(str(self.defratioy))
        
    def updated_defxratioline_edit(self):
        self.defratiox = float(self.gui.defxratiolineedit.text())
        self.defratiox_temp = float(self.gui.defxratiolineedit.text())
        self.gui.defxratioslider.setValue(1)
        
    def updated_defyratioline_edit(self):
        self.defratioy = float(self.gui.defyratiolineedit.text())
        self.defratioy_temp = float(self.gui.defyratiolineedit.text())
        self.gui.defyratioslider.setValue(1)
        
    def updated_defxratioline_editstep(self):
        self.defratiox = float(self.gui.defxratiolineedit.text())
        self.defratiox_temp = float(self.gui.defxratiolineedit.text())
        self.gui.defxratioslider.setValue(1)
        
    def updated_defyratioline_editstep(self):
        self.defratioy = float(self.gui.defyratiolineedit.text())
        self.defratioy_temp = float(self.gui.defyratiolineedit.text())
        self.gui.defyratioslider.setValue(1)
        
    def update_parameters_from_gui(self):
        '''
        '''        
        
        if self.gui.xbuttonwobble.isChecked():
            self.updefx = float(self.gui.defxwobbleamplineedit.text())*np.sin(2*np.pi*float(self.gui.defxwobblefreqlineedit.text())*self.xtime)
            self.lowdefx = self.updefx*self.defratiox
            self.xtime += 1
            
        if self.gui.xbuttonwobble.isChecked():
            self.updefy = float(self.gui.defywobbleamplineedit.text())*np.sin(2*np.pi*float(self.gui.defywobblefreqlineedit.text())*self.ytime)
            self.lowdefy = self.updefy*self.defratioy
            self.ytime += 1
        
        if self.gui.usedefratio.isChecked():
            self.lowdefx = self.updefx*self.defratiox
            self.lowdefy = self.updefy*self.defratioy
        
        self.set_deflabel()
        self.set_matrices()
            
class Biprism():
    '''Creates a biprism component and handles calls to GUI creation, updates to GUI and stores the component
    parameters. Important to note that the transfer matrix of the biprism is only cosmetic: It still
    need to be multiplied by the sign of the position of the ray to perform like a biprism. 
    '''    
    def __init__(self, z, name = '', deflection = 0.5, theta = 0, label_radius = 0.3, radius = 0.25, width = 0.01, num_points = 50):
        '''

        Parameters
        ----------
        z : float
            Position of component in optic axis
        name : str, optional
            Name of this component which will be displayed by GUI, by default ''
        deflection : float, optional
            Biprism deflection kick in slope units to the incoming ray angle, by default 0.5
        theta: int, optional
            Angle of the biprism - Two options - 0 or 1. 0 for 0 degree rotation, 1 for 90 degree rotation, by default 0
        label_radius : float, optional
            Location to place the label in the 3D GUI, by default 0.3
        radius : float, optional
            Radius of the 3D model of this component, by default 0.25
        width : float, optional
            Width of the biprism model, by default 0.01
        num_points : int, optional
            Number of points to use to make the 3D model, by default 50
        '''        
        self.type = 'Biprism'
        
        self.z = z
        self.theta = theta
        self.radius = radius 
        self.label_radius = label_radius
        self.num_points = num_points
        self.width = width
        
        self.deflection = deflection
        self.blocked_ray_idcs = []
        self.name = name
        
        self.set_gl_geom()
        self.set_gl_label()
        self.set_matrix()
        
    def biprism_matrix(self, deflection):
        '''Biprims deflection matrix - only used to store values. 

        Parameters
        ----------
        deflection : float
            update deflection kick to rays in slope coordinates

        Returns
        -------
        ndarray
            Output transfer matrix
        '''        
        matrix = np.array([[1, 0, 0, 0, 0],
                           [0, 1, 0, 0, deflection*np.sin(self.theta)],
                           [0, 0, 1, 0, 0],
                           [0, 0, 0, 1, deflection*np.cos(self.theta)],
                           [0, 0, 0, 0, 1]])

        return matrix
    
    def set_matrix(self):
        '''
        '''        
        self.matrix = self.biprism_matrix(self.deflection)
    
    def set_gl_geom(self):   
        '''
        '''        
        self.gl_points = []
        self.points = geom.biprism(self.radius, self.z, self.theta)
        self.gl_points.append(gl.GLLinePlotItem(
            pos=self.points.T, color="white", width=5))
    
    def set_gl_label(self):
        '''
        '''        
        self.label = gl.GLTextItem(pos=np.array(
            [-self.label_radius, self.label_radius, self.z]), text=self.name, color='w')
        self.label.setData(font = font)
        
    def update_geometry(self):
        '''
        '''        
        self.points = geom.biprism(self.radius, self.z, self.theta)
        self.gl_points[0].setData(pos = self.points.T)
        
    def set_gui_label(self): 
        '''
        '''        
        self.gui.deflabel.setText(
            'Biprism Deflection = ' + "{:.2f}".format(self.deflection))
        self.gui.rotlabel.setText(
            'Rotation (Radians) = ' + "{:.2f}".format(self.theta))
        self.gui.deflabel_table.setText(
            'Biprism Deflection = ' + "{:.2f}".format(self.deflection))
        self.gui.rotlabel_table.setText(
            'Rotation (Radians) = ' + "{:.2f}".format(self.theta))
        
    def create_gui(self):   
        '''
        '''        
        self.gui = BiprismGui(self.name, self.deflection, self.theta)
        
    def update_parameters_from_gui(self):
        '''
        '''        
        self.blocked_ray_idcs = []
        self.deflection = self.gui.defslider.value()*1e-3
        self.theta = self.gui.rotslider.value()*np.pi/2
        self.update_geometry()
        self.set_gui_label()
        self.set_matrix()
        
class Aperture():
    '''Creates an aperture component and handles calls to GUI creation, updates to GUI and stores the component
    parameters. Important to note that the transfer matrix of the aperture only propagates rays. The logic of 
    blocking rays is handled inside the "model" function. 
    '''

    def __init__(self, z, name = 'Aperture', aperture_radius_inner = 0.005, aperture_radius_outer = 0.25, label_radius = 0.3, num_points = 50, x = 0, y = 0):
        '''

        Parameters
        ----------
        z : float
            Position of component in optic axis
        name : str, optional
            Name of this component which will be displayed by GUI, by default 'Aperture'
        aperture_radius_inner : float, optional
           Inner radius of the aperture, by default 0.005
        aperture_radius_outer : float, optional
            Outer radius of the aperture, by default 0.25
        label_radius : float, optional
            Location to place the label in the 3D GUI, by default 0.3
        num_points : int, optional
            Number of points to use to make the 3D model, by default 50
        x : int, optional
            X position of the centre of the aperture, by default 0
        y : int, optional
            Y position of the centre of the aperture, by default 0
        '''        

        self.type = 'Aperture'
        
        self.name = name
        
        self.x = x
        self.y = y
        self.z = z

        self.aperture_radius_inner = aperture_radius_inner
        self.aperture_radius_outer = aperture_radius_outer
        self.min_radius = self.aperture_radius_inner
        self.max_radius = 0.90*self.aperture_radius_outer
        
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.set_gl_geom()
        self.set_gl_label()
        self.set_matrix()
        
        self.blocked_ray_idcs = []
        
    def create_gui(self):
        '''
        '''        
        self.gui = ApertureGui(self.name, self.min_radius, self.max_radius, self.aperture_radius_inner, self.x, self.y)
        
    def set_gl_geom(self):
        '''
        '''        
        self.gl_points = []
        
        self.verts = geom.aperture(self.aperture_radius_inner, self.aperture_radius_outer, 
                                                       self.num_points, self.num_points, self.x, self.y, self.z)
        
        self.colors = np.ones((self.verts.shape[0], 3, 4))
        self.colors[:, :, 3] = 0.2
        
        self.gl_points.append(gl.GLMeshItem(vertexes=self.verts, vertexColors=self.colors,
                                 smooth=True, drawEdges=False))
        
        self.gl_points[0].setGLOptions('additive')
        
    def update_mesh(self):
        '''
        '''        
        self.verts = geom.aperture(self.aperture_radius_inner, self.aperture_radius_outer, 
                                                       self.num_points, self.num_points, self.x, self.y, self.z)
        
        self.gl_points[0].setMeshData(vertexes=self.verts, vertexColors=self.colors,
                                 smooth=True, drawEdges=False)
        
    def set_gl_label(self):
        '''
        '''    
        self.label = gl.GLTextItem(pos=np.array(
            [-self.label_radius, self.label_radius, self.z]), text=self.name, color='w')
        self.label.setData(font = font)
        
    def set_gui_label(self):
        self.gui.radiuslabel.setText(
            'Aperture Radius = ' + "{:.4f}".format(self.aperture_radius_inner))
        self.gui.xlabel.setText(
            'Aperture X Position = ' + "{:.4f}".format(self.x))
        self.gui.ylabel.setText(
            'Aperture Y Position = ' + "{:.4f}".format(self.y))
        self.gui.radiuslabel_table.setText(
            'Aperture Radius = ' + "{:.4f}".format(self.aperture_radius_inner))
        self.gui.xlabel_table.setText(
            'Aperture X Position = ' + "{:.4f}".format(self.x))
        self.gui.ylabel_table.setText(
            'Aperture Y Position = ' + "{:.4f}".format(self.y))
        
        
    def set_matrix(self):
        '''
        '''        
        self.matrix = self.aperture_matrix
    
    def aperture_matrix(self):
        '''Aperture transfer matrix - simply a unit matrix of ones because 
        we only need to propagate rays that pass through the centre of the aperture. 

        Returns
        -------
        ndarray
            unit matrix
        '''        
        #creates a placeholder aperture matrix
        matrix = np.array([[1, 0, 0, 0, 0],
                           [0, 1, 0, 0, 0],
                           [0, 0, 1, 0, 0],
                           [0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1]])

        return matrix
    
    def update_parameters_from_gui(self):
        '''
        '''        
        self.aperture_radius_inner = self.gui.radiusslider.value()*1e-3
        self.x = self.gui.xslider.value()*1e-2
        self.y = self.gui.yslider.value()*1e-2
        self.set_gui_label()
        self.update_mesh()
        
        return

