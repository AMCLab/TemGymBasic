
import numpy as np


def circular_beam(r, outer_radius):
    '''Generates a circular paralell initial beam 

    Parameters
    ----------
    r : ndarray
        Ray position and slope matrix
    outer_radius : float
        Outer radius of the circular beam

    Returns
    -------
    r : ndarray
        Updated ray position & slope matrix which create a circular beam
    num_points_kth_ring: ndarray
        Array of the number of points on each ring of our circular beam
    '''
    num_rays = r.shape[2]

    #Use the equation from stack overflow about ukrainian graves from 2014
    #to calculate the number of even rings including decimal remainder
    num_circles_dec = (-1+np.sqrt(1+4*(num_rays)/(np.pi)))/2

    #Get the number of integer rings
    num_circles_int = int(np.floor(num_circles_dec))

    #Calculate the number of points per ring with the integer amoung of rings
    num_points_kth_ring = np.round(
        2*np.pi*(np.arange(0, num_circles_int+1))).astype(int)

    #get the remainding amount of rays
    remainder_rays = num_rays - np.sum(num_points_kth_ring)

    #Get the proportion of points in each rung
    proportion = num_points_kth_ring/np.sum(num_points_kth_ring)

    #resolve this proportion to an integer value, and reverse it
    num_rays_to_each_ring = np.ceil(proportion*remainder_rays)[::-1]

    #We need to decide on where to stop adding the remainder of rays to the rest of the rings.
    #We find this point by summing the rays in each ring from outside to inside, and then getting the index where it is greater than or equal to the remainder
    index_to_stop_adding_rays = np.where(
        np.cumsum(num_rays_to_each_ring) >= remainder_rays)[0][0]

    #We then get the total number of rays to add
    rays_to_add = np.cumsum(num_rays_to_each_ring)[
        index_to_stop_adding_rays].astype(np.int32)

    #The number of rays to add isn't always matching the remainder, so we collect them here with this line
    final_sub = rays_to_add - remainder_rays

    #Here we take them away so we get the number of rays we want
    num_rays_to_each_ring[index_to_stop_adding_rays] = num_rays_to_each_ring[index_to_stop_adding_rays] - final_sub

    #Then we add all of these rays to the correct ring
    num_points_kth_ring[::-1][:index_to_stop_adding_rays+1] = num_points_kth_ring[::-1][:index_to_stop_adding_rays+1] + num_rays_to_each_ring[:index_to_stop_adding_rays+1]

    #Add one point for the centre, and take one away from the end
    num_points_kth_ring[0] = 1
    num_points_kth_ring[-1] = num_points_kth_ring[-1] - 1

    #Make get the radii for the number of circles of rays we need
    radii = np.linspace(0, outer_radius, num_circles_int+1)

    #fill in the x and y coordinates to our ray array
    idx = 0
    for i in range(len(radii)):
       for j in range(num_points_kth_ring[i]):
           radius = radii[i]
           t = j*(2 * np.pi / num_points_kth_ring[i])
           r[0, 0, idx] = radius*np.cos(t)
           r[0, 2, idx] = radius*np.sin(t)
           idx += 1

    return r, num_points_kth_ring


def point_beam(r, beam_semi_angle):
    '''Generates a point initial beam that spreads out with semi angle 'beam_semi_angle'

    Parameters
    ----------
    r : ndarray
        Ray position and slope matrix
    beam_semi_angle : float
        Beam semi angle in radians

    Returns
    -------
    r : ndarray
        Updated ray position & slope matrix which create a circular beam
    num_points_kth_ring: ndarray
        Array of the number of points on each ring of our circular beam
    '''    
    num_rays = r.shape[2]

    #Use the equation from stack overflow about ukrainian graves
    #to calculate the number of even rings including decimal remainder
    num_circles_dec = (-1+np.sqrt(1+4*(num_rays)/(np.pi)))/2

    #Get the number of integer rings
    num_circles_int = int(np.floor(num_circles_dec))

    #Calculate the number of points per ring with the integer amoung of rings
    num_points_kth_ring = np.round(
        2*np.pi*(np.arange(0, num_circles_int+1))).astype(int)

    #get the remainding amount of rays
    remainder_rays = num_rays - np.sum(num_points_kth_ring)

    #Get the proportion of points in each rung
    proportion = num_points_kth_ring/np.sum(num_points_kth_ring)

    #resolve this proportion to an integer value, and reverse it
    num_rays_to_each_ring = np.ceil(proportion*remainder_rays)[::-1]

    #We need to decide on where to stop adding the remainder of rays to the rest of the rings.
    #We find this point by summing the rays in each ring from outside to inside, and then getting the index where it is greater than or equal to the remainder
    index_to_stop_adding_rays = np.where(
        np.cumsum(num_rays_to_each_ring) >= remainder_rays)[0][0]

    #We then get the total number of rays to add
    rays_to_add = np.cumsum(num_rays_to_each_ring)[
        index_to_stop_adding_rays].astype(np.int32)

    #The number of rays to add isn't always matching the remainder, so we collect them here with this line
    final_sub = rays_to_add - remainder_rays

    #Here we take them away so we get the number of rays we want
    num_rays_to_each_ring[index_to_stop_adding_rays] = num_rays_to_each_ring[index_to_stop_adding_rays] - final_sub

    #Then we add all of these rays to the correct ring
    num_points_kth_ring[::-1][:index_to_stop_adding_rays+1] = num_points_kth_ring[::-1][:index_to_stop_adding_rays+1] + num_rays_to_each_ring[:index_to_stop_adding_rays+1]

    #Add one point for the centre, and take one away from the end
    num_points_kth_ring[0] = 1
    num_points_kth_ring[-1] = num_points_kth_ring[-1] - 1

    #Make get the radii for the number of circles of rays we need
    radii = np.linspace(0, 1, num_circles_int+1)

    #fill in the x and y coordinates to our ray array
    idx = 0
    for i in range(len(radii)):
       for j in range(num_points_kth_ring[i]):
           radius = radii[i]
           t = j*(2 * np.pi / num_points_kth_ring[i])
           r[0, 1, idx] = np.tan(beam_semi_angle*radius)*np.cos(t)
           r[0, 3, idx] = np.tan(beam_semi_angle*radius)*np.sin(t)
           idx += 1

    return r, num_points_kth_ring


def axial_point_beam(r, beam_semi_angle):
    '''Generates a cross shaped initial beam on the x and y axis
    that spreads out with semi angle 'beam_semi_angle'

    Parameters
    ----------
    r : ndarray
        Ray position and slope matrix
    beam_semi_angle : float
        Beam semi angle in radians

    Returns
    -------
    r : ndarray
        Updated ray position & slope matrix which create a circular beam
    '''    
    num_rays = r.shape[2]

    x_rays = int(round(num_rays/2))
    x_angles = np.linspace(-beam_semi_angle, beam_semi_angle, x_rays, endpoint=True)
    y_rays = num_rays-x_rays
    y_angles = np.linspace(-beam_semi_angle, beam_semi_angle, y_rays, endpoint=True)

    for idx, angle in enumerate(x_angles):
        r[0, 1, idx] = np.tan(angle)

    for idx, angle in enumerate(y_angles):
        i = idx + y_rays
        r[0, 3, i] = np.tan(angle)

    return r


def x_axial_point_beam(r, beam_semi_angle):
    '''Generates a cross shaped initial beam on the x axis
    that spreads out with semi angle 'beam_semi_angle'

    Parameters
    ----------
    r : ndarray
        Ray position and slope matrix
    beam_semi_angle : float
        Beam semi angle in radians

    Returns
    -------
    r : ndarray
        Updated ray position & slope matrix which create a circular beam
    '''    
    num_rays = r.shape[2]

    x_rays = int(round(num_rays))
    x_angles = np.linspace(-beam_semi_angle, beam_semi_angle, x_rays, endpoint=True)

    for idx, angle in enumerate(x_angles):
        r[0, 1, idx] = np.tan(angle)

    return r


def get_image_from_rays(rays_x, rays_y, detector_size, detector_pixels):
    '''From an image of rays that hit the detector at the base of the TEM

    Parameters
    ----------
    rays_x : ndarray
        X position of rays that hit the detector
    rays_y : ndarray
        X position of rays that hit the detector
    detector_size : float
        Real size of the detector in the model. Single value that describes it's edge length.
        Note that the detector is always square
    detector_pixels : int
        Resolution of the detector.

    Returns
    -------
    detector_image : ndarray
        Image of where rays have hit the detector
    image_pixel_coords : ndarray
        Coordinates of where reach ray has hit the detector
    '''    
    detector_image = np.zeros((detector_pixels, detector_pixels), dtype=np.uint8)

    # set final image pixel coordinates
    image_pixel_coords_x = (
        np.round(rays_x / (detector_size) * detector_pixels) + detector_pixels//2-1
    ).astype(np.int32)

    image_pixel_coords_y = (
        np.round(rays_y / (detector_size) * detector_pixels) + detector_pixels//2-1
    ).astype(np.int32)

    image_pixel_coords = np.vstack([image_pixel_coords_x, image_pixel_coords_y]).T

    #Check if we have satisfied the failure mode which is for any pixel to have left the screen
    if np.any(image_pixel_coords >= detector_pixels) or np.any(image_pixel_coords < 0):
        image_pixel_coords = np.delete(image_pixel_coords, np.where(
            (image_pixel_coords < 0) | (image_pixel_coords >= detector_pixels)), axis=0)

    #Use this set of commands if you just want a white beam
    # detector_image[
    #     image_pixel_coords[:, 0],
    #     image_pixel_coords[:, 1],
    # ] += 1

    # convert the index array into a set of indices into detector_image.flat
    flat_idx = np.ravel_multi_index(image_pixel_coords.T, detector_image.shape)

    # get the set of unique indices and their corresponding counts
    uidx, ucounts = np.unique(flat_idx, return_counts=True)

    # assign the count value to each unique index in acc.flat
    detector_image.flat[uidx] = ucounts

    return detector_image, image_pixel_coords
