spnav: a ctypes wrapper for libspnav, a Space Navigator 3D mouse client

Introduction
------------

The spnav module provides a Python interface to the libspnav C
library, which allows you to read events from a Space Navigator 3D
mouse on Linux systems.  These input devices simultaneously report
linear force and rotational torque applied by the user to the device,
along with button events. See:

        http://www.3dconnexion.com/products/spacenavigator.html

for more information about the 3D navigator.


Prerequisites
-------------

As a general prerequisite to using the spnav module, you need to
install libspnav and spacenavd, available from:

        http://spacenav.sourceforge.net/

Then you need to connect a supported 3D mouse to your system.
Spacenavd supports USB devices with no configuration, but serial-based
devices will need a /etc/spnavrc configuration file.

The spnav module requires ctypes, which is standard in Python 2.5 and
later, although I have only tested spnav with Python 2.7.


Installation
------------

The spnav module installs like any other python packages.  You can
install the package from the unpacked source directory by running

  sudo python setup.up install

Quick Test
----------

To see if your installation is working, spnav comes with a test script
in the module:

  python -m spnav

This will print motion and button events from your Space Navigator to
the console.

For more information and example code, see the documentation.
