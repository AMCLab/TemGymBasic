=====
Usage
=====
Quickstart
--------
Download and run the example executable for your plafrom (Windows, MACOS or Ubuntu) from here to begun using some 
of our pre-made interactive models. 

Python
--------
To run our interactive models via python, or to create your own model, we recommend you use  `miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ installed. 
Next, install `tomoPy  <https://tomopy.readthedocs.io/en/latest/>`_ and all its runtime dependencies into a new Conda
environment called ``tomopy`` by running::

    $ conda create --name tomopy --channel conda-forge tomopy

Use this TomoPy installation by activating this environment::

    $ conda activate tomopy

then install `dxchange <https://dxchange.readthedocs.io/>`_::

	$ conda install -c conda-forge dxchange

and `tomopy cli <https://tomopycli.readthedocs.io/>`_::

    $ git clone https://github.com/tomography/tomopy-cli.git
    $ cd tomopy-cli
    $ python setup.py install

After the above installation all tomobank datasets and phantoms can be reconstructed with::

    $ tomopy recon --file-name tomo_0001.h5 --rotation-axis 1024.0