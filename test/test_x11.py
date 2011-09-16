from nose.tools import raises, assert_equals
from util import *
import spnav
from ctypes import pythonapi, c_void_p, py_object
pythonapi.PyCObject_FromVoidPtr.restype = py_object
pythonapi.PyCObject_FromVoidPtr.argtypes = [c_void_p, c_void_p]

def create_dummy_pycobject():
    return pythonapi.PyCObject_FromVoidPtr(0,0)

def test_spnav_x11_open_success():
    m = mock_libspnav({'spnav_x11_open' : 0 })
    spnav.spnav_x11_open(create_dummy_pycobject(), 0)
    assert m.spnav_x11_open.called

@raises(spnav.SpnavConnectionException)
def test_spnav_x11_open_fail():
    m = mock_libspnav({'spnav_x11_open' : -1 })
    spnav.spnav_x11_open(create_dummy_pycobject(),0)

def test_spnav_x11_window():
    m = mock_libspnav({'spnav_x11_window' : 0 })
    spnav.spnav_x11_window(0)
    assert m.spnav_x11_window.called

def test_spnav_x11_event_none():
    m = mock_libspnav({'spnav_x11_event' : 0 })
    bogus_xevent = None
    assert spnav.spnav_x11_event(bogus_xevent) is None

def test_spnav_x11_event_motion():
    def motion(xevent, event):
        fill_motion_event(event)
        return 1
    m = mock_libspnav({'spnav_x11_event' : motion })
    event = spnav.spnav_x11_event(create_dummy_pycobject())
    assert event is not None
    assert_equals(event.translation, (-1,2,-3))
    assert_equals(event.rotation, (10,-20,30))

def test_spnav_x11_event_button():
    def button(xevent, event):
        fill_button_event(event)
        return 1
    m = mock_libspnav({'spnav_x11_event' : button })
    event = spnav.spnav_x11_event(create_dummy_pycobject())
    assert event is not None
    assert_equals(event.bnum, 0)
    assert_equals(event.press, True)
