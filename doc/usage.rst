Usage
=====

Reflecting the design of ``libspnav``, the ``spnav`` Python module can
be used two ways, depending upon which protocol you use to communicate
with the Space Navigator daemon.  Both protocols emit the same event
objects.

Space Navigator Events
----------------------

Space Navigator events come in two varieties: `motion` and `button`.

Motion events result from the application of force to the 3D mouse
controller.  The strain gauges inside the controller cap can
simultaneously resolve both linear force and rotational torque, giving
6 degrees of freedom.  The linear force is reported as a signed
integer 3-vector, corresponding to the x, y, and z components of the
force.  The rotational torque is also reported as a signed integer
3-vector, with the components corresponding to torque around the x, y,
and z axis.

Button events are generated when a button on the Space Navigator
controller is pressed or released.  They consist of a button number
and a boolean indicating the type of state transition ("pressed" or
"released").

See :ref:`spnav_event_reference` for details on the event classes.

UNIX Socket Protocol
--------------------

The UNIX socket protocol is suitable when the client and daemon
process will coexist on the same computer.  It also allows for the
creation of console applications that use the Space Navigator without
an X Server.

First, the connection to the Space Navigator daemon must be opened::

  >>> from spnav import *
  >>> spnav_open()

The open connection is to a single device and global to the process.
An ``SpnavConnectionException`` will be raised if the connection cannot
be made.

Events are generated from device input by ``spacenavd`` and sent to
all connected clients.  To perform a blocking wait for the next event,
use::

  >>> event = spnav_wait_event()

.. warning:: ``spnav_wait_event()`` blocks execution inside the
   underlying C function in ``libspnav``.  As a result, the user will
   not be able to interrupt your Python application with Ctrl-C.
   ``spnav_poll_event()`` is almost always a better alternative.

To poll the library to see if an event is available, use::

  >>> event = spnav_poll_event()

If no event is available, the function returns ``None``, otherwise it
returns an event.

As long as a force is applied to the controller, ``spacenavd`` will
continuously send events to all the clients.  If your client does even
a moderate amount of computation in response to a Space Navigator
event (like rendering a 3D scene, for example), many events will queue
up before the next event can be retrieved.  This will give the
appearance of lag, as motions performed some time in the past are
processed too late.  In these situations, it is better to clear the
event queue after significant calculations::

  >>> spnav_remove_events(SPNAV_EVENT_MOTION)

Typically, only motion events should be removed, although button
events can be removed with the ``SPNAV_EVENT_BUTTON`` argument, and
both types of events can be removed from the queue with the
``SPNAV_EVENT_ANY`` option.

When finished, the socket connection is closed with::

  >>> spnav_close()


X11 Protocol
------------

The X11 protocol was defined by 3dconnexion and is used by the
official Space Navigator drivers, as well as ``spacenavd``.  It uses
the X server as a conduit to pass Space Navigator events wrapped up as
XEvents to applications, similar to other input devices.  This allows
the Space Navigator to be used with remote applications via SSH
X-Forwarding.  However, the X11 protocol can only be used with
graphical applications, as will be seen in the following example.  If
you are writing a console application, you must use the UNIX socket
protocol described above.

I have been able to successfully use the X11 protocol with `pygame
<http://pygame.org/>`_, so the remainder of this usage tutorial will
assume you are using ``pygame`` in your application.  Other windowing
toolkits may work, and you can always fall back to the UNIX socket
protocol.

Once we initialize Pygame and create a window, we can obtain the
window manager information and open the connection::

  >>> wm_info = pygame.display.get_wm_info()
  >>> spnav_x11_open(wm_info['display'], wm_info['window'])

The X11 protocol communicates with XEvents of a type that are ignored
by Pygame by default.  Next, we need to enable delivery of these events::

  >>> pygame.event.set_allowed(pygame.SYSWMEVENT)

Now Space Navigator events will be returned in a Pygame event loop::

  while True:
      for event in pygame.event.get():
          spnav_event = spnav_x11_event(event.event)
          if spnav_event is not None:
              print 'Space Navigator Event:', spnav_event

Much the same as with the UNIX socket protocol, Space Navigator events
can queue up during extended processing.  This creates a lag between
current motion by the user and the arrival of those motion events to
the front of the queue.  There is no ``spnav_remove_events()`` analog
for the X11 protocol, as the queue is handled outside of ``libspnav``.
However, one can adjust the previous event loop to only return the
most recent Space Navigator event::

  while True:
      for event in pygame.event.get(pygame.SYSWMEVENT)[-1:] \
                   + pygame.event.get():
          spnav_event = spnav_x11_event(event.event)
          if spnav_event is not None:
              print 'Space Navigator Event:', spnav_event

When finished, the connection is closed with the same function as in
the UNIX socket protocol::

  >>> spnav_close()
