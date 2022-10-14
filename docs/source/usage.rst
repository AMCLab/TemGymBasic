============
Installation
============

Quickstart Executables
----------------------
Download and run the example executable for your plafrom (Windows, MACOS or Ubuntu) from `Zenodo <https://zenodo.org/communities/amcl/?page=1&size=20>`_ to 
instantly access example models of microscope alignments without any coding knowledge.

Python
------
To run our interactive models via python, we recommend you use  `miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ .

After downloading and installing, create a new environment in a terminal::

    $ conda create --name temgymbasic python=3.9.6

activate the environment, and install pip::

    $ conda activate temgymbasic

    $ conda install pip

then install `temgymbasic <https://pypi.org/project/temgymbasic/>`_::

    $ pip install temgymbasic

To download and run the python code of examples, see our `GitHub <https://github.com/AMCLab/TemGymBasic>`_ and the folder `pyqtgraph_examples <https://github.com/AMCLab/TemGymBasic/tree/main/pyqtgraph_examples>`_.

Creating Executables
--------------------

To create the .exe files that we have shared in the zenodo,
install the package pyinstaller inside your temgymbasic environment::

    $ pip install pyinstaller

then run the appropiate terminal script, make_exe.bat (Windows) or make_exe.sh (Linux, MACOS). 
This process may take some time to create the executables for all 9 examples (~30 minutes)

