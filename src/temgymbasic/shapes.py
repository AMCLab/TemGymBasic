
import numpy as np
import triangle as tr


def square(w, x, y, z):
    '''Generates vertices for a square 3D model. Used to represent the detector

    Parameters
    ----------
    w : float
        Width of the square wire model
    x : float
        X position of the square wire model
    y : float
        Wire position of the square wire model
    z : float
        Wire position of the square wire model

    Returns
    -------
    verts3D: ndarray
        vertices to draw a 3D model
    '''
    vertices = np.array([[x + w/2, y + w/2], [x - w/2, y + w/2], [x - w/2, y - w/2],
                        [x + w/2, y - w/2], [x + w/2, y + w/2]])

    sample_dict = dict(vertices=vertices)

    sample_tri = tr.triangulate(sample_dict)

    zverts = np.ones((sample_tri['triangles'].shape[0], 3, 1), dtype=np.float32)*z
    verts_2D = sample_tri['vertices'][sample_tri['triangles']]
    verts_3D = np.dstack([verts_2D, zverts])

    return verts_3D


def deflector(r, phi, z, n_arc):
    '''Wire model geometry of deflector

    Parameters
    ----------
    r : float
        Radius of deflector geometry
    phi : float
        Angular width of deflector mode
    z : float
        Z position of deflector geometry
    n_arc : int
        Number of arcs to use to make up the model

    Returns
    -------
    points_arc_1 : ndarray
        Points of a circle to represent the lens geometry
    points_arc_2 : ndarray
        Points of a circle to represent the lens geometry
    '''

    THETA = np.linspace(-phi, phi, n_arc, endpoint=True)
    R = r*np.ones(np.size(THETA))
    Z = z*np.ones(np.size(THETA))

    points_arc_1 = np.array([R*np.cos(THETA), R*np.sin(THETA), Z])
    points_arc_2 = np.array([-R*np.cos(THETA), -R*np.sin(-THETA), Z])

    return points_arc_1, points_arc_2


def lens(r, z, n_arc):
    '''Wire model geometry of lens

    Parameters
    ----------
    r : float
        Radius of lens geometry
    z : float
        Z position of lens geometry
    n_arc : int
        Number of arcs to use to make up the model

    Returns
    -------
    points_circle : ndarray
        Points of a circle to represent the lens geometry
    '''
    THETA = np.linspace(0, 2*np.pi, n_arc, endpoint=True)
    R = r*np.ones(np.size(THETA))
    Z = z*np.ones(np.size(THETA))

    points_circle = np.array([R*np.cos(THETA), R*np.sin(THETA), Z])

    return points_circle


def biprism(r, z, theta):
    '''Wire model geometry for biprism

    Parameters
    ----------
    r : float
        Radius of wire
    z : float
        Z position of wire
    theta : float
        Angle of wire - Two options, 0 or np.pi/2

    Returns
    -------
    points : ndarray
        Points array of wire geometry
    '''
    THETA = np.array([theta, theta+np.pi])
    R = r*np.ones(np.size(THETA))
    Z = z*np.ones(np.size(THETA))

    points = np.array([R*np.cos(THETA), R*np.sin(THETA), Z])

    return points


def quadrupole(r, phi, z, n_arc):
    '''Wire model geometry of deflector

    Parameters
    ----------
    r : float
        Radius of quadrupole geometry
    phi : float
        Angular width of quadrupole mode
    z : float
        Z position of quadrupole geometry
    n_arc : int
        Number of arcs to use to make up the model

    Returns
    -------
    points_arc_1 : ndarray
        Points of first semi circle that represent the quadrupole geometry
    points_arc_2 : ndarray
        Points of second semi circle that represent the quadrupole geometry
    points_arc_3 : ndarray
        Points of third semi circle that represent the quadrupole geometry
    points_arc_4 : ndarray
        Points of fourth semi circle that represent the quadrupole geometry
    '''

    THETA = np.linspace(-phi, phi, n_arc, endpoint=True)
    R = r*np.ones(np.size(THETA))
    Z = z*np.ones(np.size(THETA))

    points_arc_1 = np.array([R*np.cos(THETA), R*np.sin(THETA), Z])
    points_arc_2 = np.array([-R*np.cos(THETA), -R*np.sin(-THETA), Z])
    points_arc_3 = np.array([R*np.cos(THETA+np.pi/2), R*np.sin(THETA+np.pi/2), Z])
    points_arc_4 = np.array([-R*np.cos(THETA+np.pi/2), -R*np.sin(-THETA+np.pi/2), Z])

    return points_arc_1, points_arc_2, points_arc_3, points_arc_4


def aperture(r_i, r_o, n_i, n_o, x, y, z):
    '''3D vertices model of an aperture

    Parameters
    ----------
    r_i : float
        Radius of inner aperture model
    r_o : float
        Radius of outer aperture model
    n_i : int
       Number of points used to represent inner aperture model
    n_o : int
        Number of points used to represent outer aperture model
    x : float
        X position of aperture
    y : float
        Y position of aperture
    z : float
        Z position of aperture

    Returns
    -------
    verts3D : ndarray
        3D array of vertices that represent the aperture model
    '''
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

    aperture_dict = dict(vertices=pts, segments=seg, holes=[[x, y]])
    aperture_tri = tr.triangulate(aperture_dict, 'qpa0.05')

    zverts = np.ones((aperture_tri['triangles'].shape[0], 3, 1), dtype=np.float32)*z
    verts_2D = aperture_tri['vertices'][aperture_tri['triangles']]
    verts_3D = np.dstack([verts_2D, zverts])

    return verts_3D
