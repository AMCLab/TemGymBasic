
from temgymbasic import components as comp
from temgymbasic.model import Model
from temgymbasic.run import run_pyqt
from temgymbasic.functions import make_test_sample, convert_rays_to_line_vertices, get_image_from_rays
from temgymbasic.run import show_matplotlib
from PyQt5.QtWidgets import QApplication
import os
import sys 
import matplotlib.pyplot as plt
import numpy as np

fourdstem_overfocused = np.load("/home/uclworkstation1/Documents/David/Code/livecalibration/fourdstem_overfocused.npy")
sample = make_test_sample()

detector_pixels = 256
detector_pixel_size = 0.000050 #pixel size in metres
detector_width = detector_pixels * detector_pixel_size

#We need to estimate the size of the sample in the sample plane,
#so We've used the scan pixel size and the number of scan positions to do so. 
scan_pixels = 128
scan_pixel_size = 0.000001 #for now assume square sample
sample_width = scan_pixels * scan_pixel_size

camera_length = 0.15
overfocus = 0.001
semiconv = 0.020
scan_rotation = 37

rec_params = {
    'overfocus': 0.001,  # m
    'scan_pixel_size': 0.000001,  # m
    'camera_length': 0.15,  # m
    'detector_pixel_size': 0.000050,  # m
    'semiconv': 0.020,  # rad
    'scan_rotation': 37,
    'flip_y': False,
}

components = [comp.DoubleDeflector(name = 'Scan Coils', z_up = 0.3, z_low = 0.25),
              comp.Lens(name = 'Lens', z = 0.20, f = -0.05),
              comp.Sample(name = 'Sample', sample = sample, z = camera_length, width = sample_width),
              comp.DoubleDeflector(name = 'Descan Coils', z_up = 0.1, z_low = 0.05, scan_rotation = scan_rotation)
              ]

model = Model(components, beam_z = 0.4, beam_type = 'paralell', num_rays = 2**14, 
              experiment = '4DSTEM', detector_pixels = detector_pixels, 
              detector_size = detector_width)

model.scan_pixel_size = scan_pixel_size
model.scan_pixels = 4

model.set_beam_radius_from_semiconv(semiconv)
model.set_obj_lens_f_from_overfocus(overfocus)
model.generate_rays()
num_sample_positions = model.scan_pixels**2

# show_matplotlib(model)

for _ in range(num_sample_positions-1):
    
    model.update_scan_position()
    model.update_scan_coil_ratio()
    model.step()
    
    #Create detector image of rays
    detector_ray_image, detector_sample_image, _ = get_image_from_rays(
        model.r[-1, 0, :], model.r[-1, 2, :], 
        model.r[model.sample_r_idx, 0, :], model.r[model.sample_r_idx, 2, :], 
        model.detector_size, model.detector_pixels,
        model.components[model.sample_idx].sample_size, model.components[model.sample_idx].sample_pixels,
        model.components[model.sample_idx].sample
        )
    
plt.figure()
plt.imshow(detector_sample_image)

plt.figure()
plt.imshow(fourdstem_overfocused[64, 64, :, :])


    
