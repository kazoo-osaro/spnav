'''spnav: a ctypes wrapper for libspnav, a Space Navigator 3D mouse client'''

from ctypes import cdll, c_int, c_uint, c_void_p, py_object, byref, \
    Structure, Union, pythonapi

# OMG CALLING CPYTHON FUNCTIONS FROM INSIDE PYTHON
pythonapi.PyCObject_AsVoidPtr.restype = c_void_p
pythonapi.PyCObject_AsVoidPtr.argtypes = [py_object]

libspnav = cdll.LoadLibrary('libspnav.so')

SPNAV_EVENT_ANY = 0
SPNAV_EVENT_MOTION = 1
SPNAV_EVENT_BUTTON = 2

class spnav_event_motion(Structure):
    '''Space Navigator motion event C struct

    A motion event is produced whenever a force is applied to the 3D mouse.

    Fields:

      type: int
        Always set to SPNAV_EVENT_MOTION

      x, y, z: int
        Linear translation force.  Sign of value indicates direction.

      rx, ry, rz: int
        Rotation force around each axis.  Sign of value indicates direction.

      period: unsigned int

      data: c_void_p
        Raw event data.  Ignore this field.
    '''
    _fields_ = [('type', c_int),
                ('x', c_int),
                ('y', c_int),
                ('z', c_int),
                ('rx', c_int),
                ('ry', c_int),
                ('rz', c_int),
                ('period', c_uint),
                ('data', c_void_p)]

class spnav_event_button(Structure):
    '''Space Navigator button event C struct

    A button event is produced whenever a button on the 3D mouse is pressed
    or released.

    Fields:

      type: int
        Always set to SPNAV_EVENT_BUTTON

      press: int
        Set to 1 when the button is pressed and 0 when released.

      bnum: int
        Button number on device.
    '''
    _fields_ = [('type', c_int),
                ('press', c_int),
                ('bnum', c_int)]

class spnav_event(Union):
    '''Space Navigator Event

    A C union between the motion and button event structs.

      type: int
        SPNAV_EVENT_MOTION or SPNAV_EVENT_BUTTON
      
      motion: spnave_event_motion,
        If ``type`` == ``SPNAV_EVENT_MOTION``, then this
        is a motion event C struct.

      button: spnave_event_button,
        If ``type`` == ``SPNAV_EVENT_BUTTON``, then this
        is a motion event C struct.
    '''
    _fields_ = [('type', c_int),
                ('motion', spnav_event_motion),
                ('button', spnav_event_button) ]

    def __str__(self):
        if self.type == SPNAV_EVENT_ANY:
            return 'SPNAV_EVENT_ANY'
        elif self.type == SPNAV_EVENT_MOTION:
            motion = self.motion
            return 'SPNAV_EVENT_MOTION t(%d,%d,%d) r(%d,%d,%d)' \
                % (motion.x, motion.y, motion.z, 
                   motion.rx, motion.ry, motion.rz)
        elif self.type == SPNAV_EVENT_BUTTON:
            if self.button.press:
                state = 'down'
            else:
                state = 'up'
            return 'SPNAV_EVENT_BUTTON %d %s' % (self.button.bnum, state)

class SpnavException(Exception):
    '''Base class for all ``spnav`` exceptions.'''
    def __init__(self, msg):
        Exception.__init__(self, msg)

class SpnavConnectionException(SpnavException):
    '''Exception caused by failure to connect to source of spnav events.'''
    def __init__(self, msg):
        SpnavException.__init__(self, msg)

class SpnavWaitException(SpnavException):
    '''Exception caused by error while waiting for spnav event to arrive.'''
    def __init__(self, msg):
        SpnavException.__init__(self, msg)
    
def spnav_open():
    '''Open connection to the daemon via AF_UNIX socket.

    The unix domain socket interface is an alternative to the original
    magellan protocol, and it is *NOT* compatible with the 3D
    connexion driver. If you wish to remain compatible, use the X11
    protocol (spnav_x11_open, see below).

    Raises ``SpnavConnectionException`` if connection cannot be established.
    '''
    if libspnav.spnav_open() == -1:
        raise SpnavConnectionException(
            'failed to connect to the space navigator daemon')

def spnav_fd():
    '''Retrieves the file descriptor used for communication with the
    daemon, for use with select() by the application, if so required.
    If the X11 mode is used, the socket used to communicate with the X
    server is returned, so the result of this function is always
    reliable.  If AF_UNIX mode is used, the fd of the socket is
    returned or -1 if no connection is open / failure occured.'''
    return libspnav.spnav_fd()

def spnav_close():
    '''Closes connection to the daemon.'''
    libspnav.spnav_close()

def spnav_x11_open(display, window):
    '''Opens a connection to the daemon, using the original magellan
    X11 protocol.  Any application using this protocol should be
    compatible with the proprietary 3D connexion driver too.'''
    display_ptr = pythonapi.PyCObject_AsVoidPtr(display)
    if libspnav.spnav_x11_open(display_ptr, window) == -1:
        raise SpnavConnectionException(
            'failed to connect to the space navigator daemon')

def spnav_x11_window(window):
    '''Sets the application window, that is to receive events by the driver.
 
    NOTE: Any number of windows can be registered for events, when
    using the free spnavd daemon. The libspnav author suspects that
    the proprietary 3D connexion daemon only sends events to one
    window at a time, thus this function replaces the window that
    receives events. If compatibility with 3dxsrv is required, do not
    assume that you can register multiple windows.'''
    libspnav.spnav_x11_window(window)

def spnav_wait_event():
    '''Blocks waiting for Space Navigator events.

       Note that the block happens inside the libspnav library, so you
       will not be able to interrupt this function with Ctrl-C.  It is
       almost always better to use spnav_poll_event() instead.

       Returns an instance of ``spnav_event``.
    '''
    event = spnav_event()
    ret = libspnav.spnav_wait_event(byref(event))
    if ret:
        return event
    else:
        raise SpnavWaitException('non-zero return code from spnav_wait_event()')

def spnav_poll_event():
    '''Polls for waiting for Space Navigator events.

       Returns: None if no waiting events, otherwise an instance of
       ``spnav_event``.
    '''
    event = spnav_event()
    ret = libspnav.spnav_poll_event(byref(event))
    if ret == 0:
        return None
    else:
        return event

def spnav_remove_events(event_type):
    '''Removes pending Space Navigator events from the queue.

      This function is useful to purge old events that may have
      queued up after a long calculation.  It helps to keep
      your application appearing more responsive.

      event_type: int
        The type of events to remove.  SPNAV_EVENT_MOTION or
        SPNAV_EVENT_BUTTON removes just motion or button events,
        respectively.  SPSPNAV_EVENT_ANY removes both types of events.
    '''
    return libspnav.spnav_remove_events(event_type)

def spnav_x11_event(xevent):
    '''Examines an arbitrary X11 event to see if it is a Space
    Navigator event.

    Returns: None if not a Space Navigator event, otherwise
    an instance of spnav_event is returned.
    '''
    event = spnav_event()
    ret = libspnav.spnav_x11_event(xevent, byref(event))
    if ret == 0:
        return None
    else:
        return event
