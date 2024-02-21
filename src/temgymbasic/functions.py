
import numpy as np


def make_test_sample(size=256):
    # Code From Dieter Weber
    obj = np.ones((size, size), dtype=np.complex64)
    y, x = np.ogrid[-size//2:size//2, -size//2:size//2]

    outline = (
        ((y*1.2)**2 + x**2) > (110/256*size)**2
    ) & (
        (((y*1.2)**2 + x**2) < (120/256*size)**2)
    )
    obj[outline] = 0.0

    left_eye = ((y + 40/256*size)**2 + (x + 40/256*size)**2) < (20/256*size)**2
    obj[left_eye] = 0
    right_eye = (np.abs(y + 40/256*size) < 15/256*size) & (np.abs(x - 40/256*size) < 30/256*size)
    obj[right_eye] = 0

    nose = (y + 20/256*size + x > 0) & (x < 0) & (y < 10/256*size)

    obj[nose] = (0.05j * x + 0.05j * y)[nose]

    mouth = (
        ((y*1)**2 + x**2) > (50/256*size)**2
    ) & (
        (((y*1)**2 + x**2) < (70/256*size)**2)
    ) & (
        y > 20/256*size
    )

    obj[mouth] = 0

    tongue = (
        ((y - 50/256*size)**2 + (x - 50/256*size)**2) < (20/256*size)**2
    ) & (
        (y**2 + x**2) > (70/256*size)**2
    )
    obj[tongue] = 0

    # This wave modulation introduces a strong signature in the diffraction pattern
    # that allows to confirm the correct scale and orientation.
    signature_wave = np.exp(1j*(3 * y + 7 * x) * 2*np.pi/size)

    obj += 0.3*signature_wave - 0.3

    return np.abs(obj)


# FIXME resolve code duplication between circular_beam() and point_beam()
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

    # Use the equation from stack overflow about ukrainian graves from 2014
    # to calculate the number of even rings including decimal remainder
    num_circles_dec = (-1+np.sqrt(1+4*(num_rays)/(np.pi)))/2

    # Get the number of integer rings
    num_circles_int = int(np.floor(num_circles_dec))

    # Calculate the number of points per ring with the integer amoung of rings
    num_points_kth_ring = np.round(
        2*np.pi*(np.arange(0, num_circles_int+1))).astype(np.int32)

    # get the remainding amount of rays
    remainder_rays = num_rays - np.sum(num_points_kth_ring)

    # Get the proportion of points in each rung
    proportion = num_points_kth_ring/np.sum(num_points_kth_ring)

    # resolve this proportion to an integer value, and reverse it
    num_rays_to_each_ring = np.ceil(proportion*remainder_rays)[::-1].astype(np.int32)

    # We need to decide on where to stop adding the remainder of rays to the
    # rest of the rings. We find this point by summing the rays in each ring
    # from outside to inside, and then getting the index where it is greater
    # than or equal to the remainder
    index_to_stop_adding_rays = np.where(
        np.cumsum(num_rays_to_each_ring) >= remainder_rays)[0][0]

    # We then get the total number of rays to add
    rays_to_add = np.cumsum(num_rays_to_each_ring)[
        index_to_stop_adding_rays].astype(np.int32)

    # The number of rays to add isn't always matching the remainder, so we
    # collect them here with this line
    final_sub = rays_to_add - remainder_rays

    # Here we take them away so we get the number of rays we want
    num_rays_to_each_ring[index_to_stop_adding_rays] -= final_sub

    # Then we add all of these rays to the correct ring
    num_points_kth_ring[::-1][:index_to_stop_adding_rays+1] += num_rays_to_each_ring[
        :index_to_stop_adding_rays+1
    ]

    # Add one point for the centre, and take one away from the end
    num_points_kth_ring[0] = 1
    num_points_kth_ring[-1] = num_points_kth_ring[-1] - 1

    # Make get the radii for the number of circles of rays we need
    radii = np.linspace(0, outer_radius, num_circles_int+1)

    # fill in the x and y coordinates to our ray array
    idx = 0
    for i in range(len(radii)):
        for j in range(num_points_kth_ring[i]):
            radius = radii[i]
            t = j*(2 * np.pi / num_points_kth_ring[i])
            r[0, 0, idx] = radius*np.cos(t)
            r[0, 2, idx] = radius*np.sin(t)
            idx += 1

    return r, num_points_kth_ring


def point_beam(r, gun_beam_semi_angle):
    '''Generates a point initial beam that spreads out with semi angle 'gun_beam_semi_angle'

    Parameters
    ----------
    r : ndarray
        Ray position and slope matrix
    gun_beam_semi_angle : float
        Beam semi angle in radians

    Returns
    -------
    r : ndarray
        Updated ray position & slope matrix which create a circular beam
    num_points_kth_ring: ndarray
        Array of the number of points on each ring of our circular beam
    '''
    num_rays = r.shape[2]

    # Use the equation from stack overflow about ukrainian graves
    # to calculate the number of even rings including decimal remainder
    num_circles_dec = (-1+np.sqrt(1+4*(num_rays)/(np.pi)))/2

    # Get the number of integer rings
    num_circles_int = int(np.floor(num_circles_dec))

    # Calculate the number of points per ring with the integer amoung of rings
    num_points_kth_ring = np.round(
        2*np.pi*(np.arange(0, num_circles_int+1))).astype(np.int32)

    # get the remainding amount of rays
    remainder_rays = num_rays - np.sum(num_points_kth_ring)

    # Get the proportion of points in each rung
    proportion = num_points_kth_ring/np.sum(num_points_kth_ring)

    # resolve this proportion to an integer value, and reverse it
    num_rays_to_each_ring = np.ceil(proportion*remainder_rays)[::-1].astype(np.int32)

    # We need to decide on where to stop adding the remainder of rays to the
    # rest of the rings. We find this point by summing the rays in each ring
    # from outside to inside, and then getting the index where it is greater
    # than or equal to the remainder
    index_to_stop_adding_rays = np.where(
        np.cumsum(num_rays_to_each_ring) >= remainder_rays)[0][0]

    # We then get the total number of rays to add
    rays_to_add = np.cumsum(num_rays_to_each_ring)[
        index_to_stop_adding_rays].astype(np.int32)

    # The number of rays to add isn't always matching the remainder, so we
    # collect them here with this line
    final_sub = rays_to_add - remainder_rays

    # Here we take them away so we get the number of rays we want
    num_rays_to_each_ring[index_to_stop_adding_rays] -= final_sub

    # Then we add all of these rays to the correct ring
    num_points_kth_ring[::-1][:index_to_stop_adding_rays+1] += num_rays_to_each_ring[
        :index_to_stop_adding_rays+1
    ]

    # Add one point for the centre, and take one away from the end
    num_points_kth_ring[0] = 1
    num_points_kth_ring[-1] = num_points_kth_ring[-1] - 1

    # Make get the radii for the number of circles of rays we need
    radii = np.linspace(0, 1, num_circles_int+1)

    # fill in the x and y coordinates to our ray array
    idx = 0
    for i in range(len(radii)):
        for j in range(num_points_kth_ring[i]):
            radius = radii[i]
            t = j*(2 * np.pi / num_points_kth_ring[i])
            r[0, 1, idx] = np.tan(gun_beam_semi_angle*radius)*np.cos(t)
            r[0, 3, idx] = np.tan(gun_beam_semi_angle*radius)*np.sin(t)
            idx += 1

    return r, num_points_kth_ring


def axial_point_beam(r, gun_beam_semi_angle):
    '''Generates a cross shaped initial beam on the x and y axis
    that spreads out with semi angle 'gun_beam_semi_angle'

    Parameters
    ----------
    r : ndarray
        Ray position and slope matrix
    gun_beam_semi_angle : float
        Beam semi angle in radians

    Returns
    -------
    r : ndarray
        Updated ray position & slope matrix which create a circular beam
    '''
    num_rays = r.shape[2]

    x_rays = int(round(num_rays/2))
    x_angles = np.linspace(-gun_beam_semi_angle, gun_beam_semi_angle, x_rays, endpoint=True)
    y_rays = num_rays-x_rays
    y_angles = np.linspace(-gun_beam_semi_angle, gun_beam_semi_angle, y_rays, endpoint=True)

    for idx, angle in enumerate(x_angles):
        r[0, 1, idx] = np.tan(angle)

    for idx, angle in enumerate(y_angles):
        i = idx + y_rays
        r[0, 3, i] = np.tan(angle)

    return r


def x_axial_point_beam(r, gun_beam_semi_angle):
    '''Generates a cross shaped initial beam on the x axis
    that spreads out with semi angle 'gun_beam_semi_angle'

    Parameters
    ----------
    r : ndarray
        Ray position and slope matrix
    gun_beam_semi_angle : float
        Beam semi angle in radians

    Returns
    -------
    r : ndarray
        Updated ray position & slope matrix which create a circular beam
    '''
    num_rays = r.shape[2]

    x_rays = int(round(num_rays))
    x_angles = np.linspace(-gun_beam_semi_angle, gun_beam_semi_angle, x_rays, endpoint=True)

    for idx, angle in enumerate(x_angles):
        r[0, 1, idx] = np.tan(angle)

    return r


def _flip_y():
    # From libertem.corrections.coordinates v0.11.1
    return np.array([
        (-1, 0),
        (0, 1)
    ])


def _identity():
    # From libertem.corrections.coordinates v0.11.1
    return np.eye(2)


def _rotate(radians):
    # From libertem.corrections.coordinates v0.11.1
    # https://en.wikipedia.org/wiki/Rotation_matrix
    # y, x instead of x, y
    return np.array([
        (np.cos(radians), np.sin(radians)),
        (-np.sin(radians), np.cos(radians))
    ])


def _rotate_deg(degrees):
    # From libertem.corrections.coordinates v0.11.1
    return _rotate(np.pi/180*degrees)


def get_pixel_coords(rays_x, rays_y, size, pixels, flip_y=False, scan_rotation=0.):
    if flip_y:
        transform = _flip_y()
    else:
        transform = _identity()

    # Transformations are applied right to left
    transform = _rotate_deg(scan_rotation) @ transform

    y_transformed, x_transformed = (np.array((rays_y, rays_x)).T @ transform).T

    pixel_coords_x = x_transformed / size * pixels + pixels/2 - 1
    pixel_coords_y = y_transformed / size * pixels + pixels/2 - 1

    return (pixel_coords_x, pixel_coords_y)


def get_image_from_rays(
        rays_x, rays_y, sample_rays_x, sample_rays_y, detector_size,
        detector_pixels, sample_size, sample_pixels, sample_image,
        flip_y=True):
    '''From an image of rays that hit the detector at the base of the TEM

    Parameters
    ----------
    rays_x : ndarray
        X position of rays that hit the detector
    rays_y : ndarray
        X position of rays that hit the detector
    sample_rays_x : ndarray
        X position of rays that hit the sample
    sample_rays_y : ndarray
        Y position of rays that hit the sample
    detector_size : float
        Real size of the detector in the model. Single value that describes it's edge length.
        Note that the detector is always square
    detector_pixels : int
        Pixel resolution of the detector
    sample_size : float
        Real size of the sample in the model. Single value that describes it's edge length.
        Note that the sample is always square
    sample_pixels : int
        Pixel resolution of the the sample
    sample_image : ndarray
        image intensities of the sample. Used to form an image on the detector
    Returns
    -------
    detector_ray_image : ndarray
        Ray image of where rays have hit the detector
    detector_sample_image : ndarray
        Sample image obtained by transferring ray which have hit the detector
    sample_pixel_coords : ndarray
        Coordinates of where each ray has hit the sample
    detector_pixel_coords : ndarray
        Coordinates of where each ray has hit the detector
    '''
    detector_ray_image = np.zeros((detector_pixels, detector_pixels), dtype=np.uint8)
    detector_sample_image = np.zeros((detector_pixels, detector_pixels))

    # Convert rays from sample positions to pixel positions
    sample_pixel_coords_x, sample_pixel_coords_y = np.round(get_pixel_coords(
        rays_x=sample_rays_x,
        rays_y=sample_rays_y,
        size=sample_size,
        pixels=sample_pixels,
        flip_y=flip_y
    )).astype(np.int32)

    sample_pixel_coords = np.vstack([sample_pixel_coords_x, sample_pixel_coords_y]).T

    # Convert rays from detector positions to pixel positions
    detector_pixel_coords_x, detector_pixel_coords_y = np.round(get_pixel_coords(
        rays_x=rays_x,
        rays_y=rays_y,
        size=detector_size,
        pixels=detector_pixels,
        flip_y=flip_y
    )).astype(np.int32)

    detector_pixel_coords = np.vstack([detector_pixel_coords_x, detector_pixel_coords_y]).T
    sample_rays_inside = np.all(
        (sample_pixel_coords > 0) & (sample_pixel_coords < sample_pixels), axis=1
    ).T
    detector_rays_inside = np.all(
        (detector_pixel_coords > 0) & (detector_pixel_coords < detector_pixels), axis=1
    ).T
    rays_that_hit_sample_and_detector = (sample_rays_inside & detector_rays_inside)
    rays_that_hit_detector_but_not_sample = (~sample_rays_inside & detector_rays_inside)

    sample_pixel_intensities = sample_image[
            sample_pixel_coords[rays_that_hit_sample_and_detector, 1],
            sample_pixel_coords[rays_that_hit_sample_and_detector, 0]
    ]

    # Return this image for the case when we want to just plot the beam on the detector
    detector_ray_image[
        detector_pixel_coords[rays_that_hit_detector_but_not_sample, 1],
        detector_pixel_coords[rays_that_hit_detector_but_not_sample, 0],
    ] += 1

    # Obtain sample image intensitions
    detector_sample_image[
        detector_pixel_coords[rays_that_hit_sample_and_detector, 1],
        detector_pixel_coords[rays_that_hit_sample_and_detector, 0]
    ] = sample_pixel_intensities
    detector_sample_image[
        detector_pixel_coords[rays_that_hit_detector_but_not_sample, 1],
        detector_pixel_coords[rays_that_hit_detector_but_not_sample, 0]
    ] = 0

    return detector_ray_image, detector_sample_image, sample_pixel_coords, detector_pixel_coords


def convert_rays_to_line_vertices(model):
    '''Converts a ray position matrix of size [(steps, 5, num rays)] -
    (where steps is defined by the number of components + 2 - the two being
    included to add the gun and detector, which are not components chosen by the user)'
    to a line matrix of shape [(steps)*2-2)*num rays, 3], which is of the correct shape
    to be readily plot ray positions in the column as lines.

    Parameters
    ----------
    model : class
        Microscope model that stores all associated ray position data
    gun_beam_semi_angle : float
        Beam semi angle in radians

    Returns
    -------
    r : ndarray
        Updated ray position & slope matrix which create a circular beam
    '''
    ray_z = np.tile(model.z_positions, [model.num_rays, 1, 1]).T

    # Stack with the z coordinates
    ray_xyz = np.hstack((model.r[:, [0, 2], :], ray_z))

    # Repeat vertices so we can create lines. The shape of this array is [Num Steps*2, 3, Num Rays]
    lines_repeated = np.repeat(ray_xyz[:, :, :], repeats=2, axis=0)[1:-1]

    # Index the total number of rays in the model initially which are by default
    # allowed through all components
    allowed_rays = range(model.num_rays)

    for component in model.components:
        if len(component.blocked_ray_idcs) != 0:
            # Find the difference between blocked rays and original amount of allowed rays
            allowed_rays = list(set(allowed_rays).difference(set(component.blocked_ray_idcs)))
            # Convert from ray position indexing, to line indexing
            idx = component.index*2+2
            # Get the coordinates of all rays which hit the aperture.
            pts_blocked = lines_repeated[idx, :, component.blocked_ray_idcs]
            # Do really funky array manipulation to create a copy of all of
            # these points that is the same shape as the vertices of remaining
            # lines after the aperture (I'm sorry to myself and anyone in the
            # future who has to read this)
            lines_aperture = np.broadcast_to(
                pts_blocked[..., None], pts_blocked.shape+(lines_repeated.shape[0]-(idx),)
            ).transpose(2, 1, 0)

            # Copy the coordinate of all rays that hit the aperture, to all line
            # vertices after this, so we don't visualise them.
            lines_repeated[idx:, :, component.blocked_ray_idcs] = lines_aperture

    # Then restack each line so that we end up with a long list of lines, from
    # [Num Steps*2, 3, Num Rays] > [(Num Steps*2-2)*Num rays, 3]
    # see > https://stackoverflow.com/questions/38509196/efficiently-re-stacking-a-numpy-ndarray
    lines_paired = lines_repeated.transpose(2, 0, 1).reshape(
        lines_repeated.shape[0]*model.num_rays, 3)

    return lines_paired, allowed_rays
