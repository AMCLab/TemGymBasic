#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 14:37:00 2022

@author: andy
"""
import numpy as np
import triangle as tr

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

def aperture(r_i, r_o, n_i, n_o, z):
    
    i_i = np.arange(n_i)
    i_o = np.arange(n_o)
    theta_i = i_i * 2 * np.pi / n_i
    theta_o = i_o * 2 * np.pi / n_o
    pts_inner = np.stack([np.cos(theta_i), np.sin(theta_i)], axis=1) * r_i
    pts_outer = np.stack([np.cos(theta_o), np.sin(theta_o)], axis=1) * r_o
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




