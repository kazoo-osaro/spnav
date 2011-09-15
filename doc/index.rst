.. spnav documentation master file, created by
   sphinx-quickstart on Thu Sep 15 16:28:11 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

spnav: Space Navigator support in Python
========================================

The ``spnav`` module provides a Python interface to the ``libspnav`` C
library, which allows you to read events from a Space Navigator 3D
mouse on Linux systems.  These input devices simultaneously report
linear force and rotational torque applied by the user to the device,
along with button events. See:

        http://www.3dconnexion.com/products/spacenavigator.html

for more information about the 3D navigator.

Any device supported by ``spacenavd`` is supported by the ``libspnav``
and therefore the spnav module.  This includes not only the current
USB devices sold by 3dconnexion, but older serial-based devices that
were sold under many brand names.

For more information about ``spacenavd`` and ``libspnav``, see:

        http://spacenav.sourceforge.net/

Documentation
=============

.. toctree::
   :maxdepth: 2

   setup
   usage
   reference

Development
===========

The source repository for ``spnav`` is located at:

        http://bitbucket.org/seibert/spnav/

You can download the source code with Mercurial:

::
  hg clone http://bitbucket.org/seibert/spnav/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

