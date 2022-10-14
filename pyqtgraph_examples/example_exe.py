from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from collections import OrderedDict
import sys

import beam_tilt_shift_basic_example_pyqt
import beam_tilt_shift_advanced_example_pyqt
import condenser_aperture_example_pyqt
import lens_example_pyqt
import model_sem_example_pyqt
import model_tem_example_pyqt
import condenser_astigmatism_example_pyqt
import biprism_example_pyqt

# sys.path.insert(1, r"G:\My Drive\Davids Research\LinearTEM\LINEARTEMGYM-master_\LINEARTEMGYM-master\temgym\src")

examples = OrderedDict([
    ('Basic Beam Tilt/Shift', beam_tilt_shift_basic_example_pyqt),
    ('Advanced Beam Tilt/Shift', beam_tilt_shift_advanced_example_pyqt),
    ('Simple Lens', lens_example_pyqt),
    ('Split Biprism', biprism_example_pyqt),
    ('Model SEM', model_sem_example_pyqt),
    ('Model TEM', model_tem_example_pyqt),
    ('Condenser Aperture', condenser_aperture_example_pyqt),
    ('Condenser Astigmatism', condenser_astigmatism_example_pyqt)
])

#Code to make a .exe that can run scripts in the same folder with the push of a button. 
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.viewer = None
        
        #make the GUI layout
        self.layout = QVBoxLayout(self)
        self.createbuttons()

    def createbuttons(self):
        #loop through list of example items, and connect them to a button.
        for idx, (key, val) in enumerate(examples.items()):
            button = QPushButton(key, self)
            button.clicked.connect(lambda ch, val=val: self.runfile(val))
            self.layout.addWidget(button)

    def runfile(self, file):
        if self.viewer is None:
            self.viewer = file.main()
            self.viewer.show()
        else:
            self.viewer.close()  # Close windoviewer.
            self.viewer = None  # Discard reference.
    

if __name__ == "__main__":
    mainapp = MainWindow()
    mainapp.show()

    
    
    
