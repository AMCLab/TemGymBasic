#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 26 16:43:42 2022

@author: andy
"""

import numpy as np
from functions import circular_beam, point_beam, axial_point_beam
from gui import ModelGui


class buildmodel():
    
    def __init__(self, components, beam_z = 1, num_rays = 256, beam_type = 'point', beam_semi_angle = np.pi/4, beam_tilt_x = 0, beam_tilt_y = 0):
        self.components = components
        self.num_rays = num_rays
        self.beam_width = 0.2
        self.beam_z = beam_z
        self.beam_type = beam_type
        self.beam_semi_angle = beam_semi_angle

        self.beam_tilt_x = beam_tilt_x
        self.beam_tilt_y = beam_tilt_y

        self.set_z_positions()
        self.z_distances = np.diff(self.z_positions)
        self.generate_rays()
        self.update_component_matrix()
        self.allowed_ray_idcs = np.arange(self.num_rays)
        
        self.detector_size = 0.5
        self.detector_pixels = 128
            
    def set_z_positions(self):
        self.z_positions = []
        self.z_positions.append(self.beam_z)
        
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
            
        self.z_positions.append(0)
        
    def create_gui(self):
        self.gui = ModelGui(self.num_rays, self.beam_type, self.beam_semi_angle, self.beam_tilt_x, self.beam_tilt_y)
        
    def generate_rays(self):
        self.steps = len(self.z_positions)
        self.r = np.zeros((self.steps, 5, self.num_rays), dtype = np.float64) #x, theta_x, y, theta_y, 1
        self.r[:, 4, :] = np.ones(self.num_rays)
        
        if self.beam_type == 'paralell':
            self.r, self.spot_indices = circular_beam(self.r, self.beam_width)
        elif self.beam_type == 'point':
            self.r, self.spot_indices = point_beam(self.r, self.beam_semi_angle)
        elif self.beam_type == 'axial':
            self.r = axial_point_beam(self.r, self.beam_semi_angle)
        
        self.r[:, 1, :]+=self.beam_tilt_x
        self.r[:, 3, :]+=self.beam_tilt_y

    def update_component_matrix(self):
        self.components_matrix = []
        for idx, component in enumerate(self.components):  
            if component.type == 'Double Deflector':
                self.components_matrix.append(component.up_matrix)
                self.components_matrix.append(component.low_matrix)
            else:
                self.components_matrix.append(component.matrix)
            
    def update_rays_stepwise(self):
        
        self.r[1, :, :] = np.matmul(self.propagate(self.z_distances[0]), self.r[0, :, :])
        idx = 1
        for component in self.components:
            if component.type == 'Biprism':
                if component.theta != 0:
                    x = abs(self.r[idx, 0, :])
                    y = abs(self.r[idx, 2, :])
                    x_hit_biprism = np.where(x<component.width)[0]
                    y_hit_biprism = np.where(y<component.radius)[0]
                    
                    blocked_idcs = list(set(x_hit_biprism).intersection(y_hit_biprism))

                elif component.theta == 0:
                    x = abs(self.r[idx, 0, :])
                    y = abs(self.r[idx, 2, :])
                    x_hit_biprism = np.where(x<component.radius)[0]
                    y_hit_biprism = np.where(y<component.width)[0]
                    
                    blocked_idcs = list(set(x_hit_biprism).intersection(y_hit_biprism))
                    
                component.blocked_ray_idcs = blocked_idcs
                
                self.r[idx, 1, :] = self.r[idx, 1, :]+np.sign(self.r[idx, 0, :])*component.matrix[1, 4]
                self.r[idx, 3, :] = self.r[idx, 3, :]+np.sign(self.r[idx, 2, :])*component.matrix[3, 4]
                self.r[idx+1, :, :] = np.matmul(self.propagate(self.z_distances[idx]), self.r[idx, :, :])
                idx += 1
                
            elif component.type == 'Aperture':
                radii = np.hypot(*self.r[idx, [0, 2], :])
                component.blocked_ray_idcs = np.where(radii >= component.aperture_radius_inner)[0]
                
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
        self.num_rays = 2**(self.gui.rayslider.value())
        self.beam_semi_angle = self.gui.beamangleslider.value()*1e-3
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
        self.update_component_matrix()
        self.update_rays_stepwise()
        
        return self.r
    
    def propagate(self, z):
        
        matrix = np.array([[1, z, 0, 0, 0],
                           [0, 1, 0, 0, 0],
                           [0, 0, 1, z, 0],
                           [0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 1]])
        
        return matrix