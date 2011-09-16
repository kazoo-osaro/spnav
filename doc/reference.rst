Reference
=========

.. py:currentmodule:: spnav

The ``spnav`` module interface exactly mirrors the C API of
``libspnav``, but the C union of event structs has been replaced with
Python classes.

.. _spnav_event_reference:

Event Classes
-------------

Event types are identified by module constants:

.. py:data:: SPNAV_EVENT_MOTION

Linear and rotation force applied to controller.

.. py:data:: SPNAV_EVENT_BUTTON

Button pressed or released.

.. py:data:: SPNAV_EVENT_ANY

Either motion or button event.  Only used with ``spnav_remove_events``.

.. autoclass:: SpnavEvent
.. autoclass:: SpnavMotionEvent
.. autoclass:: SpnavButtonEvent

UNIX Socket Protocol
--------------------

.. autofunction:: spnav_open
.. autofunction:: spnav_wait_event
.. autofunction:: spnav_poll_event
.. autofunction:: spnav_remove_events
.. autofunction:: spnav_close

X11 Socket Protocol
-------------------

.. autofunction:: spnav_x11_open
.. autofunction:: spnav_x11_event
.. autofunction:: spnav_close

Exceptions
----------

.. autoexception:: SpnavException 
.. autoexception:: SpnavConnectionException 
.. autoexception:: SpnavWaitException
