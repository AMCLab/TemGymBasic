#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 14:37:00 2022

@author: andy
"""
import numpy as np
import triangle as tr

def square(w, x, y, z):
    
    vertices = np.array([[x + w/2, y + w/2], [x - w/2, y + w/2], [x - w/2, y - w/2],
                        [x + w/2, y - w/2], [x + w/2, y + w/2]])

    sample_dict = dict(vertices=vertices)
    
    sample_tri = tr.triangulate(sample_dict)

    zverts = np.ones((sample_tri['triangles'].shape[0], 3, 1), dtype=np.float32)*z
    verts_2D = sample_tri['vertices'][sample_tri['triangles']]
    verts_3D = np.dstack([verts_2D, zverts])
    
    return verts_3D

    
def deflector(r, phi, z, n_arc):
    
    THETA = np.linspace(-phi, phi, n_arc, endpoint = True) 
    R = r*np.ones(np.size(THETA))
    Z = z*np.ones(np.size(THETA))
    
    points_arc_1 = np.array([R*np.cos(THETA), R*np.sin(THETA), Z])
    points_arc_2 = np.array([-R*np.cos(THETA), -R*np.sin(-THETA), Z])
    
    return points_arc_1, points_arc_2

def lens(r, z, n_arc):
    
    THETA = np.linspace(0, 2*np.pi, n_arc, endpoint = True) 
    R = r*np.ones(np.size(THETA))
    Z = z*np.ones(np.size(THETA))
    
    points_circle = np.array([R*np.cos(THETA), R*np.sin(THETA), Z])

    return points_circle

def biprism(r, z, theta):
    
    THETA = np.array([theta, theta+np.pi])
    R = r*np.ones(np.size(THETA))
    Z = z*np.ones(np.size(THETA))
    
    points_circle = np.array([R*np.cos(THETA), R*np.sin(THETA), Z])

    return points_circle

def quadrupole(r, phi, z, n_arc):
    
    THETA = np.linspace(-phi, phi, n_arc, endpoint = True) 
    R = r*np.ones(np.size(THETA))
    Z = z*np.ones(np.size(THETA))
    
    points_arc_1 = np.array([R*np.cos(THETA), R*np.sin(THETA), Z])
    points_arc_2 = np.array([-R*np.cos(THETA), -R*np.sin(-THETA), Z])
    points_arc_3 = np.array([R*np.cos(THETA+np.pi/2), R*np.sin(THETA+np.pi/2), Z])
    points_arc_4 = np.array([-R*np.cos(THETA+np.pi/2), -R*np.sin(-THETA+np.pi/2), Z])
    
    return points_arc_1, points_arc_2, points_arc_3, points_arc_4

def aperture(r_i, r_o, n_i, n_o, x, y, z):
    
    i_i = np.arange(n_i)
    i_o = np.arange(n_o)
    theta_i = i_i * 2 * np.pi / n_i
    theta_o = i_o * 2 * np.pi / n_o
    pts_inner = np.stack([x + np.cos(theta_i)*r_i, y + np.sin(theta_i)*r_i], axis=1)
    pts_outer = np.stack([x + np.cos(theta_o)*r_o, y + np.sin(theta_o)*r_o], axis=1)
    seg_i = np.stack([i_i, i_i + 1], axis=1) % n_i
    seg_o = np.stack([i_o, i_o + 1], axis=1) % n_o
    
    pts = np.vstack([pts_outer, pts_inner])
    seg = np.vstack([seg_o, seg_i + seg_o.shape[0]])
    
    aperture_dict = dict(vertices=pts, segments=seg, holes=[[0, 0]])
    aperture_tri = tr.triangulate(aperture_dict, 'qpa0.05')

    zverts = np.ones((aperture_tri['triangles'].shape[0], 3, 1), dtype=np.float32)*z
    verts_2D = aperture_tri['vertices'][aperture_tri['triangles']]
    verts_3D = np.dstack([verts_2D, zverts])
    
    return verts_3D




