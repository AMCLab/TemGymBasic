from PyQt5.QtWidgets import QApplication
import sys
from main import LinearTEMUi, LinearTEMCtrl
from components import Lens, Deflector, DoubleDeflector, Biprism, Aperture
from model import BuildModel
from pyqtgraph.Qt import QtCore

AppWindow = QApplication(sys.argv)

components = [Lens(name = 'Lens', z = 0.8),
              DoubleDeflector(name = 'Double Deflector', z_up = 0.75, z_low = 0.7),
              Deflector(name = 'Deflector', z = 0.6, defx = 0, defy = 0),
              Biprism(name = 'Biprism', z = 0.4),
              Aperture(name = 'Aperture', z = 0.1, aperture_radius_inner = 0.01)]

model = BuildModel(components, beam_type = 'point', num_rays = 32, beam_semi_angle = 0.03)
view = LinearTEMUi(model)
ctrl = LinearTEMCtrl(model, view)
view.show()

sys.exit(AppWindow.exec_())


