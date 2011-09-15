from ctypes import cdll, c_int, c_uint, c_void_p, py_object, byref, Structure, Union, pythonapi

# OMG CALLING CPYTHON FUNCTIONS FROM INSIDE PYTHON
pythonapi.PyCObject_AsVoidPtr.restype = c_void_p
pythonapi.PyCObject_AsVoidPtr.argtypes = [py_object]

libspnav = cdll.LoadLibrary('libspnav.so')

SPNAV_EVENT_ANY = 0
SPNAV_EVENT_MOTION = 1
SPNAV_EVENT_BUTTON = 2

class spnav_event_motion(Structure):
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
    _fields_ = [('type', c_int),
                ('press', c_int),
                ('bnum', c_int)]

class spnav_event(Union):
    _fields_ = [('type', c_int),
                ('motion', spnav_event_motion),
                ('button', spnav_event_button) ]

    def __str__(self):
        if self.type == SPNAV_EVENT_ANY:
            return 'SPNAV_EVENT_ANY'
        elif self.type == SPNAV_EVENT_MOTION:
            m = self.motion
            return 'SPNAV_EVENT_MOTION t(%d,%d,%d) r(%d,%d,%d)' % (m.x, m.y, m.z, m.rx, m.ry, m.rz)
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

class SpnavConnectionException(Exception):
    '''Exception caused by failure to connect to source of spnav events.'''
    def __init__(self, msg):
        SpnavException.__init__(self, msg)

class SpnavWaitException(Exception):
    '''Exception caused by error while waiting for spnav event to arrive.'''
    def __init__(self, msg):
        SpnavException.__init__(self, msg)
    
def spnav_open():
    if libspnav.spnav_open() == -1:
        raise SpnavConnectionException('failed to connect to the space navigator daemon')

def spnav_fd():
    return libspnav.spnav_fd()

def spnav_close():
    libspnav.spnav_close()

def spnav_x11_open(display, window):
    display_ptr = pythonapi.PyCObject_AsVoidPtr(display)
    if libspnav.spnav_x11_open(display_ptr, window) == -1:
        raise SpnavConnectionException('failed to connect to the space navigator daemon')

def spnav_x11_window(window):
    libspnav.spnav_x11_window(window)

def spnav_wait_event():
    ev = spnav_event()
    ret = libspnav.spnav_wait_event(byref(ev))
    if ret:
        return ev
    else:
        raise SpnavWaitException('non-zero return code from spnav_wait_event()')

def spnav_poll_event():
    ev = spnav_event()
    ret = libspnav.spnav_poll_event(byref(ev))
    if ret == 0:
        return None
    else:
        return ev

def spnav_remove_events(event_type):
    return libspnav.spnav_remove_events(event_type)

def spnav_x11_event(xevent):
    ev = spnav_event()
    ret = libspnav.spnav_x11_event(xevent, byref(ev))
    if ret == 0:
        return None
    else:
        return ev
