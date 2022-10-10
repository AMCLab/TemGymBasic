
import numpy as np
from temgymbasic.functions import circular_beam, point_beam, axial_point_beam, x_axial_point_beam
from temgymbasic.gui import ModelGui

'''This class create the model composed of the specified components, and handles all of the computation
that transmits the rays through each component.'''
class Model():
    '''Generates a model electron microscope. This class generates performs the matrix 
    multiplication and function updates to calculate their positions throughout
    the column.
    '''
    def __init__(self, components, beam_z=1, num_rays=256, beam_type='point', 
                 beam_semi_angle=np.pi/4, beam_tilt_x=0, beam_tilt_y=0, beam_width = 0.2,
                 detector_size = 0.5, detector_pixels = 128):
        '''

        Parameters
        ----------
        components : list
            List of components to electron microscope component to input into the model
        beam_z : int, optional
            Sets the initial height of the beam, by default 1
        num_rays : int, optional
            Sets the number of rays generated at the beam_z position. A large 
            number of rays will in general slow down the programme quite a lot. , by default 256
        beam_type : str, optional
            Choose the type of beam:
                    -'point' beam creates a set of rays that start from a single point and 
                     spread out like a cone.
                    -'paralell' beam creates a set of rays that start from the same position, but 
                    each have the same angle.
                    - 'axial' creates a beam which is only visible on the x and y axis.
                    - 'x_axial' creates a beam which is only visible on the x-axis. This is only used 
                    for matplotlib diagrams, by default 'point'
        beam_semi_angle : float, optional
            Set the semi angle of the beam in radians., by default np.pi/4
        beam_tilt_x : int, optional
            Set the tilt of the beam in the x direction, by default 0
        beam_tilt_y : int, optional
            Set the tilt of the beam in the y direction, by default 0
        beam_width : float, optional
            Set the width of the beam - only matters if "paralell" beam type is selected
        detector_size : float, optional
            Set the size of the detector, by default 0.5
        detector_pixels : int, optional
            Set the number of pixels in the detector. A large number of pixels will 
            probably considerably hinder performance, by default 128
        '''        
        self.components = components
        self.num_rays = num_rays
        self.beam_width = beam_width
        self.beam_z = beam_z
        self.beam_type = beam_type
        self.beam_semi_angle = beam_semi_angle

        self.beam_tilt_x = beam_tilt_x
        self.beam_tilt_y = beam_tilt_y
        
        #Need a special function for creating the z_positions of each component because and
        #double deflector is composed of two components, so we need to account for that. 
        self.set_z_positions()
        
        self.z_distances = np.diff(self.z_positions)
        
        #Make the matrix of rays that depends on the beam conditions input into the model.
        self.generate_rays()
        self.update_component_matrix()
        self.allowed_ray_idcs = np.arange(self.num_rays)

        self.detector_size = detector_size
        self.detector_pixels = detector_pixels

    def set_z_positions(self):
        '''Create the z position list of all components in the model
        '''        
        self.z_positions = []
        
        #Input the initial beam_z as the first z_position
        self.z_positions.append(self.beam_z)
        
        #We need to loop through all components and where there is a double deflector,
        #we need to add an extra z_position to the matrix
        double_deflectors = 0
        for idx, component in enumerate(self.components):
            if component.type == 'Double Deflector':
                self.z_positions.append(component.z_up)
                component.index = idx
                self.z_positions.append(component.z_low)
                component.index = idx + 1
                double_deflectors += 1
            else:
                self.z_positions.append(component.z)
                component.index = idx + double_deflectors
                
        #Add the position of the detector
        self.z_positions.append(0)
    
    #Create the ModelGUI if we are running pyqtgraph
    def create_gui(self):
        '''Create the GUI
        '''        
        self.gui = ModelGui(self.num_rays, self.beam_type,
                            self.beam_semi_angle, self.beam_tilt_x, self.beam_tilt_y)

    def generate_rays(self):
        '''Generate electron rays
        '''        
        #Make our 3D matrix of rays. This matrix is of shape (steps, 5, num rays), where
        #steps is defined by the number of components.
        
        self.steps = len(self.z_positions)
        self.r = np.zeros((self.steps, 5, self.num_rays),
                          dtype=np.float64)  # x, theta_x, y, theta_y, 1
        self.r[:, 4, :] = np.ones(self.num_rays)

        if self.beam_type == 'paralell':
            self.r, self.spot_indices = circular_beam(self.r, self.beam_width)
        elif self.beam_type == 'point':
            self.r, self.spot_indices = point_beam(self.r, self.beam_semi_angle)
        elif self.beam_type == 'axial':
            self.r = axial_point_beam(self.r, self.beam_semi_angle)
        elif self.beam_type == 'x_axial':
            self.r = x_axial_point_beam(self.r, self.beam_semi_angle)

        self.r[:, 1, :] += self.beam_tilt_x
        self.r[:, 3, :] += self.beam_tilt_y
    
    #Add the matrices of each component to a list
    def update_component_matrix(self):
        '''Update the matrix of each component 
        '''        
        self.components_matrix = []
        for idx, component in enumerate(self.components):
            if component.type == 'Double Deflector':
                self.components_matrix.append(component.up_matrix)
                self.components_matrix.append(component.low_matrix)
            else:
                self.components_matrix.append(component.matrix)
    
    #Perform the matrix multiplication of the rays with each component in the model
    def update_rays_stepwise(self):
        '''Perform the neccessary matrix multiplications and function multiplications
        to propagate the beam through the column
        '''        
        #Do the matrix multiplication of the first rays with the distance between the beam z 
        #and the first component
        self.r[1, :, :] = np.matmul(self.propagate(self.z_distances[0]), self.r[0, :, :])
        
        idx = 1
        
        #For every component, loop through it and perform the matrix multiplication
        for component in self.components:
            if component.type == 'Biprism':
                x = abs(self.r[idx, 0, :])
                y = abs(self.r[idx, 2, :])
                if component.theta != 0:

                    x_hit_biprism = np.where(x < component.width)[0]
                    y_hit_biprism = np.where(y < component.radius)[0]

                elif component.theta == 0:
                    x_hit_biprism = np.where(x < component.radius)[0]
                    y_hit_biprism = np.where(y < component.width)[0]

                blocked_idcs = list(set(x_hit_biprism).intersection(y_hit_biprism))

                component.blocked_ray_idcs = blocked_idcs

                self.r[idx, 1, :] = self.r[idx, 1, :] + \
                    np.sign(self.r[idx, 0, :])*component.matrix[1, 4]
                self.r[idx, 3, :] = self.r[idx, 3, :] + \
                    np.sign(self.r[idx, 2, :])*component.matrix[3, 4]
                self.r[idx+1, :, :] = np.matmul(self.propagate(self.z_distances[idx]), self.r[idx, :, :])
                idx += 1

            elif component.type == 'Aperture':
                
                #Special vectorised function for the aperture
                xp, yp = self.r[idx, 0, :], self.r[idx, 2, :]
                xc, yc = component.x, component.y
                distance = np.sqrt((xp-xc)**2 + (yp-yc)**2)

                blocked_ray_bools = np.logical_and(
                    distance >= component.aperture_radius_inner, distance < component.aperture_radius_outer)
                component.blocked_ray_idcs = np.where(blocked_ray_bools)[0]

                self.r[idx+1, :, :] = np.matmul(self.propagate(self.z_distances[idx]), self.r[idx, :, :])
                idx += 1
            elif component.type == 'Double Deflector':
                self.r[idx, :, :] = np.matmul(component.up_matrix, self.r[idx, :, :])
                self.r[idx+1, :, :] = np.matmul(self.propagate(self.z_distances[idx]), self.r[idx, :, :])
                idx += 1

                self.r[idx, :, :] = np.matmul(component.low_matrix, self.r[idx, :, :])
                self.r[idx+1, :, :] = np.matmul(self.propagate(self.z_distances[idx]), self.r[idx, :, :])
                idx += 1
            else:
                self.r[idx, :, :] = np.matmul(component.matrix, self.r[idx, :, :])
                self.r[idx+1, :, :] = np.matmul(self.propagate(self.z_distances[idx]), self.r[idx, :, :])
                idx += 1

    def update_gui(self):
        '''Update the GUI
        '''        
        #This code updates the GUI sliders
        self.num_rays = 2**(self.gui.rayslider.value())
        self.beam_semi_angle = self.gui.beamangleslider.value()*1e-2
        self.beam_width = self.gui.beamwidthslider.value()*1e-3
        self.allowed_ray_idcs = np.arange(self.num_rays)

        self.beam_tilt_x = self.gui.xangleslider.value()*np.pi*1e-3
        self.beam_tilt_y = self.gui.yangleslider.value()*np.pi*1e-3

        if self.gui.checkBoxAxial.isChecked():
            self.beam_type = 'axial'
        if self.gui.checkBoxParalell.isChecked():
            self.beam_type = 'paralell'
        if self.gui.checkBoxPoint.isChecked():
            self.beam_type = 'point'

        self.set_model_labels()
        self.generate_rays()

    def set_model_labels(self):
        '''Set labels of the model inside the GUI
        '''        
        self.gui.raylabel.setText(
            str(self.num_rays))
        self.gui.beamanglelabel.setText(
            str(round(self.beam_semi_angle, 2)))
        self.gui.beamwidthlabel.setText(
            str(round(self.beam_width, 2)))

        self.gui.xanglelabel.setText(
            str('Beam Tilt X (Radians) = ' + "{:.3f}".format(self.beam_tilt_x))
        )
        self.gui.yanglelabel.setText(
            str('Beam Tilt Y (Radians) = ' + "{:.3f}".format(self.beam_tilt_y))
        )

    def step(self):
        '''Master function that updates the matrices and perfroms ray propagation

        Returns
        -------
        r : ndarray
            Returns the array of ray positions
        '''        
        #This method performs the computation of updating the matrices to their gui slider 
        #paramaters, and of moving the rays throgh the model.
        self.update_component_matrix()
        self.update_rays_stepwise()

        return self.r
    
    #Propagation matrix used by the model to propagate rays between components
    def propagate(self, z):
        '''Propagation matrix

        Parameters
        ----------
        z : float
            Distance to propagate rays

        Returns
        -------
        ndarray
            Propagation matrix
        '''        

        matrix = np.array([[1, z, 0, 0, 0],
                           [0, 1, 0, 0, 0],
                           [0, 0, 1, z, 0],
                           [0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1]])

        return matrix
