
import geometry as geom
from gui import *
import pyqtgraph.opengl as gl
import numpy as np
from PyQt5.QtGui import QFont

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
        self.gui.flabel.setText(
            'Focal Length = ' + "{:.2f}".format(self.f))
        
    def create_gui(self):
        '''
        '''        
        self.gui = LensGui(self.name + ' Interface', self.f)
        
    def update_gui(self):
        '''
        '''        
        '''Update method called by the main loop of the programme
        '''        
        self.f = self.gui.fslider.value()*1e-3

        if self.gui.fwobble.isChecked():
            self.f += np.abs(np.sin(-1*2*np.pi*3e-2*self.ftime))*-0.6
            self.ftime += 1

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
        self.fy = fy

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
        
    def set_flabel(self):
        '''
        '''        
        self.gui.fxlabel.setText(
            self.gui_label + 'X = ' + "{:.2f}".format(self.fx))
        self.gui.fylabel.setText(
            self.gui_label + 'Y = ' + "{:.2f}".format(self.fy))
        
    def create_gui(self): 
        '''
        '''        
        self.gui = AstigmaticLensGui(self.name + ' Interface', self.gui_label, self.fx, self.fy)
        
    def update_gui(self):
        '''
        '''        
        self.fx = self.gui.fxslider.value()*1e-3
        self.fy = self.gui.fyslider.value()*1e-3
        self.set_flabel()
        self.set_matrix()
        
    

class Sample():
    '''Creates a sample component which serves only as a visualisation on the 3D model. 
    '''    
    def __init__(self, z, name = '', label_radius = 0.3, width = 0.25, num_points = 50, x = 0., y = 0.):
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
            X position of sample model, by default 0
        y : int, optional
            Y position of sample model, by default 0
        '''        

        self.type = 'Sample'
        
        self.x = x
        self.y = y
        self.z = z
        self.width = width 
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.blocked_ray_idcs = []
        self.name = name
        self.set_matrix()
        self.set_gl_geom()
        self.set_gl_label()
        
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
        
    def create_gui(self): 
        '''
        '''         
        self.gui = SampleGui(self.name + ' Interface', self.x, self.y)

    def set_gl_label(self): 
        '''
        '''        
        self.label = gl.GLTextItem(pos=np.array(
            [-self.label_radius, self.label_radius, self.z]), text=self.name, color='w')
        self.label.setData(font = font)
    
    def update_mesh(self):
        '''
        '''        
        self.verts = geom.square(self.width, self.x, self.y, self.z)
        
        self.gl_points[0].setMeshData(vertexes=self.verts, vertexColors=self.colors,
                                 smooth=True, drawEdges=False)
        
    def update_gui(self):
        '''
        '''        
        self.x = self.gui.xslider.value()*1e-2
        self.y = self.gui.yslider.value()*1e-2
        self.update_mesh()
    
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
            Focal length of this quadrupole in x, by default -0.5
        fx : float, optional, 
            Focal length of this quadrupole in y, by default -0.5
        label_radius : float, optional
            Location to place the label in the 3D GUI, by default 0.3
        radius : float, optional
            Radius of the 3D model of this component, by default 0.25
        num_points : int, optional
            Number of points to use to make the 3D model, by default 50
        '''        
        self.type = 'Quadrupole'
        self.gui_label = 'Stigmator Strength '
        self.z = z
        self.radius = radius 
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.fx = fx
        self.fy = fy

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
        
    def set_flabel(self):
        '''
        '''        
        self.gui.fxlabel.setText(
            self.gui_label + 'X = ' + "{:.2f}".format(self.fx))
        self.gui.fylabel.setText(
            self.gui_label + 'Y = ' + "{:.2f}".format(self.fy))
        
    def create_gui(self):
        '''
        '''        
        self.gui = AstigmaticLensGui(self.name + ' Interface', self.type, self.fx, self.fy)
        
    def update_gui(self):
        '''
        '''        
        self.fx = self.gui.fxslider.value()*1e-3
        self.fy = self.gui.fyslider.value()*1e-3
        self.set_flabel()
        self.set_matrix()

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
        self.gui.defxlabel.setText(
            'X Deflection = ' + "{:.2f}".format(self.defx))
        self.gui.defylabel.setText(
            'Y Deflection = ' + "{:.2f}".format(self.defy))
        
    def create_gui(self):  
        '''
        '''        
        self.gui = DeflectorGui(self.name + ' Interface', self.defx, self.defy)
        
    def update_gui(self):
        '''
        '''        
        self.defx = self.gui.defxslider.value()*1e-3
        self.defy = self.gui.defyslider.value()*1e-3
        self.set_deflabel()
        self.set_matrix()
        
class DoubleDeflector():
    '''Creates a double deflector component and handles calls to GUI creation, updates to GUI
        and stores the component matrix. Primarily used in the Beam Tilt/Shift alignment.
    '''    
    def __init__(self, z_up, z_low, name = '', updefx = 0.0, updefy = 0.0, lowdefx = 0.0, lowdefy = 0.0, label_radius = 0.3, radius = 0.25, num_points = 50):
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
        self.radius = radius
        self.label_radius = label_radius
        self.num_points = num_points
        
        self.updefx = updefx
        self.updefy = updefy
        
        self.lowdefx = lowdefx
        self.lowdefy = lowdefy
        
        self.defratiox = 0
        self.defratioy = 0
        
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
    
    def set_matrices(self):
        '''
        '''        
        self.up_matrix = self.deflector_matrix(self.updefx, self.updefy)
        self.low_matrix = self.deflector_matrix(self.lowdefx, self.lowdefy)
    
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
        self.gui.updefxlabel.setText(
            'X Deflection = ' + "{:.2f}".format(self.updefx))
        self.gui.updefylabel.setText(
            'Y Deflection = ' + "{:.2f}".format(self.updefy))
        self.gui.lowdefxlabel.setText(
            'X Deflection = ' + "{:.2f}".format(self.lowdefx))
        self.gui.lowdefylabel.setText(
            'Y Deflection = ' + "{:.2f}".format(self.lowdefy))
        self.gui.defratioxlabel.setText(
            'Lower Deflector X Response Ratio = ' + "{:.2f}".format(self.defratiox))
        self.gui.defratioylabel.setText(
            'Lower Deflector Y Response Ratio = ' + "{:.2f}".format(self.defratioy))
        
    def create_gui(self):
        '''
        '''        
        self.gui = DoubleDeflectorGui(self.name + ' Interface', self.updefx, self.updefy, self.lowdefx, self.lowdefy)
        
    def update_gui(self):
        '''
        '''        
        self.updefx = self.gui.updefxslider.value()*1e-3
        self.updefy = self.gui.updefyslider.value()*1e-3
        self.lowdefx = self.gui.lowdefxslider.value()*1e-3
        self.lowdefy = self.gui.lowdefyslider.value()*1e-3
        self.defratiox = self.gui.defratioxslider.value()*1e-3
        self.defratioy = self.gui.defratioyslider.value()*1e-3
        
        if self.gui.xbuttonwobble.isChecked():
            self.updefx = (np.sin(-1*2*np.pi*1e-2*self.xtime))
            
            self.lowdefx = self.updefx*self.defratiox
            self.xtime += 1
        if self.gui.ybuttonwobble.isChecked():
            self.updefy = (np.sin(-1*2*np.pi*1e-2*self.ytime))
            self.lowdefy = self.updefy*self.defratioy
            self.ytime += 1
        
        self.set_deflabel()
        self.set_matrices()
        
class Biprism():
    '''Creates a biprism component and handles calls to GUI creation, updates to GUI and stores the component
    parameters. Important to note that the transfer matrix of the biprism is only cosmetic: It still
    need to be multiplied by the sign of the position of the ray to perform like a biprism. 
    '''    
    def __init__(self, z, name = '', deflection = 0.5, theta = 0., label_radius = 0.3, radius = 0.25, width = 0.01, num_points = 50):
        '''

        Parameters
        ----------
        z : float
            Position of component in optic axis
        name : str, optional
            Name of this component which will be displayed by GUI, by default ''
        deflection : float, optional
            Biprism deflection kick in slope units to the incoming ray angle, by default 0.5
        theta : float, optional
            Angle of the biprism - Two options - 0 or np.pi/2, by default 0
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
        
    def create_gui(self):   
        '''
        '''        
        self.gui = BiprismGui(self.name + ' Interface', self.deflection, self.theta)
        
    def update_gui(self):
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
        self.gui = ApertureGui(self.name + ' Interface', self.min_radius, self.max_radius, self.aperture_radius_inner, self.x, self.y)
        
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
    
    def update_gui(self):
        '''
        '''        
        self.aperture_radius_inner = self.gui.radiusslider.value()*1e-3
        self.x = self.gui.xslider.value()*1e-2
        self.y = self.gui.yslider.value()*1e-2
        self.set_gui_label()
        self.update_mesh()
        
        return

