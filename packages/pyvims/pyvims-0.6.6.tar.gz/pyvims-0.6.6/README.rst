PyVIMS
===============================

|Build| |PyPI| |Status| |Version| |Python| |License|

.. |Build| image:: https://travis-ci.org/seignovert/pyvims.svg?branch=master
        :target: https://travis-ci.org/seignovert/pyvims
.. |PyPI| image:: https://img.shields.io/badge/PyPI-pyvims-blue.svg
        :target: https://pypi.org/project/pyvims
.. |Status| image:: https://img.shields.io/pypi/status/pyvims.svg?label=Status
        :target: https://pypi.org/project/pyvims
.. |Version| image:: https://img.shields.io/pypi/v/pyvims.svg?label=Version
        :target: https://pypi.org/project/pyvims
.. |Python| image:: https://img.shields.io/pypi/pyversions/pyvims.svg?label=Python
        :target: https://pypi.org/project/pyvims
.. |License| image:: https://img.shields.io/pypi/l/pyvims.svg?label=License
        :target: https://pypi.org/project/pyvims

Python package to manipulate the Cassini VIMS data.

Prerequisites
--------------
This module use ``GDAL`` library to create and load ``GeoTIFF`` files.
You need to install it first before installing ``pyvims``.

With ``conda``:

.. code:: bash

    $ conda config --add channels conda-forge
    $ conda install -c conda-forge gdal

Or directly on Ubuntu:

.. code:: bash
    
    $ apt-get install libgdal-dev

For other operating system, please refer to OSGeo_ page.

.. _OSGeo: https://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries

Install
-------
With ``pip``:

.. code:: bash

    $ pip install pyvims

With the ``source files``:

.. code:: bash

    $ git clone https://github.com/seignovert/pyvims.git
    $ cd pyvims ; python setup.py install

Testing
-------
Check the install:

.. code:: python

    >>> from pyvims import VIMS

Examples
--------
Download test files (ISIS3 cubes of ``1487096932_1``):

.. code:: bash

    $ wget https://vims.univ-nantes.fr/data/isis/003TI/C1487096932_1_vis.cub
    $ wget https://vims.univ-nantes.fr/data/isis/003TI/C1487096932_1_ir.cub
    $ wget https://vims.univ-nantes.fr/data/isis/003TI/N1487096932_1_vis.cub
    $ wget https://vims.univ-nantes.fr/data/isis/003TI/N1487096932_1_ir.cub

To use, simply do:

.. code:: python

    >>> from pyvims import VIMS
    >>> cub = VIMS('1487096932_1')

    >>> cub
    VIMS cube: 1487096932_1 [ISIS3]

    >>> cub.time
    '2005-02-14T18:05:00.976500'

    >>> cub.target
    u'TITAN'

    >>> cub.NS, cub.NL
    (42, 42)

For more details, take a look to the
`Jupyter NoteBook <https://nbviewer.jupyter.org/github/seignovert/pyvims/blob/master/pyvims.ipynb>`_
where more example of usage are provided.

Dependencies
------------
- Numpy
- DateTime
- CV2
- Piexif
- PVL_ (`patched issue #34 <https://github.com/planetarypy/pvl/pull/34>`_)
- PlanetaryImage
- SpiceyPy

.. _PVL: https://github.com/seignovert/pvl
