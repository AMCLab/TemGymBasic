============================
Ray Diagrams with Matplotlib
============================

Model TEM 
---------

The same code which creates an interactive model via pyqtgraph of the specified microscope components 
can also be used to create a static ray diagram in matplotlib. The highlighted lines show the changes that need 
to me made to create a matplotlib diagram rather than in an interactive pyqtgraph model. 

.. literalinclude:: ../../matplotlib_examples/model_tem_example_matplotlib.py
   :language: python
   :emphasize-lines: 5,33-36

which produces this model:

.. image:: model_tem.svg
   :width: 600px
   :alt: project

