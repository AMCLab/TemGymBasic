from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from collections import OrderedDict
import sys
import subprocess
import numpy as np

examples = OrderedDict([
    ('Advanced Beam Tilt/Shift', 'beam_tilt_shift_advanced_example_pyqt.py'),
    ('Simple Lens', 'lens_example_pyqt.py'),
    ('Split Biprism', 'biprism_example_pyqt.py'),
    ('Model SEM', 'model_sem_example_pyqt.py'),
    ('Model TEM', 'model_tem_example_pyqt.py'),
    ('Condenser Aperture', 'condenser_aperture_example_pyqt.py'),
    ('Condenser Astigmatism', 'condenser_astigmatism_example_pyqt.py')
])

#Code to make a .exe that can run scripts in the same folder with the push of a button. 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        #make the GUI layout
        self.layout = QVBoxLayout(self)
        self.createbuttons()
        self.show()

    def createbuttons(self):
        #loop through list of example items, and connect them to a button.
        for idx, (key, val) in enumerate(examples.items()):
            button = QPushButton(key, self)
            button.clicked.connect(lambda ch, val=val: self.runfile(val))
            self.layout.addWidget(button)

    def runfile(self, file):
        #Open a new subprocess and run the python script.
        subprocess.Popen(['python', file])


if __name__ == '__main__':
    AppWindow = QApplication(sys.argv)
    mainapp = MainWindow()
    sys.exit(AppWindow.exec_())
