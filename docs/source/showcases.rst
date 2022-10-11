===========================
Showcase Interactive Models
===========================

The models presented below showcase some of the other modelling capabilities of our software.

Biprism
-------
We can combine three biprism components created in our software to make an interactive
version of the microscope setup presented in this paper from tonamura in 2012.

.. image:: /source/img/biprism_model.png
   :width: 600px
   :alt: project

Model TEM
---------
Adopting a qualitative schematic found here for a JEOL 2010F Transmission Electron Microscope, 
we can recreate an interactive alignment model of this microscope using the components we have created. 
The code which creates this model is located in the python script ''model_tem_example_pyqt.py''

.. literalinclude:: /pyqtgraph_examples/model_tem_example_pyqt.py
   :language: python

.. image:: /source/img/model_tem_example.png
   :width: 600px
   :alt: project

Model SEM
---------
Also simply using a SEM schematic found on wikipedia, we can also easily recreate an alignment model of 
showing how the beam inside a scanning electron microscope operates.

.. literalinclude:: /pyqtgraph_examples/model_sem_example_pyqt.py
   :language: python

.. image:: /source/img/model_sem_example.png
   :width: 600px
   :alt: project
