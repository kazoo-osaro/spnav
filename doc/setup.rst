Setup
=====

Prerequisites
-------------

To access a Space Navigator (or compatible) device in Linux, you need
to run a daemon in the background.  The official 3dconnexion drivers
provide such a server, but the open source `spacenav
<http://spacenav.sourceforge.net/>`_ project provides a vastly
superior daemon that I highly recommend.

``spacenavd`` can communicate input events with client software using
either the X11-based protocol supported by the 3dconnexion drivers, or
a local UNIX socket-based protocol.  The ``libspnav`` client library,
also produced by the `spacenav` project, can use either protocol.

If you are using Ubuntu 11.04, you can install ``spacenavd`` and
``libspnav`` with the following command::

  sudo apt-get install spacenavd libspnav0

Otherwise, you will need to download the sofware from:

        http://spacenav.sourceforge.net

and install it manually.

Package Installation
--------------------

The ``spnav`` Python module can installed from PyPI with the command::

  sudo easy_install spnav

or installed from `source <http://bitbucket.org/seibert/spnav/>`_ by
running the usual Python installation procedure::

  sudo python setup.py install

The ``spnav`` module requires ``ctypes``, which is standard in Python 2.5 and
later, although I have only tested spnav with Python 2.7.


Tips
----

* ``spacenavd`` supports USB devices with no additional configuration
  file, but serial devices do need the port name set in
  ``/etc/spnavrc``.

* Neither ``spacenavd`` nor the 3dconnexion damon support more than
  one Space Navigator device connected to a single computer.

* Serial devices may have a different convention for the orientation
  of the y and z axes.  You might need to flip them in the
  configuration file.

* The X11-based protocol works automatically with X11 forwarding and
  SSH, allowing you to send input events to software running on a
  remote computer.  Note that ``libspnav`` and the ``spnav`` Python
  module need to be installed on the remote computer for this to work.

* If you experience strange permission problems when the ``spacenavd``
  daemon is started automatically by the Ubuntu boot scripts.  If you
  are having trouble, stop the daemon::

    sudo service spacenavd stop

  and then start the daemon manually from a X terminal window::

    sudo spacenavd

  Alternatively, try using the direct UNIX socket protocol.
