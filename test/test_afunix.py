from nose.tools import raises, assert_equals
import spnav
from util import *

def test_spnav_open_success():
    m = mock_libspnav({'spnav_open' : 0 })
    spnav.spnav_open()
    assert m.spnav_open.called

@raises(spnav.SpnavConnectionException)
def test_spnav_open_fail():
    m = mock_libspnav({'spnav_open' : -1 })
    spnav.spnav_open()

def test_spnav_fd():
    m = mock_libspnav({'spnav_fd' : 0 })
    spnav.spnav_fd()
    assert m.spnav_fd.called

def test_spnav_close():
    m = mock_libspnav({'spnav_close' : 0 })
    spnav.spnav_close()
    assert m.spnav_close.called

def test_spnav_remove_events():
    m = mock_libspnav({'spnav_remove_events' : 0 })
    spnav.spnav_remove_events(spnav.SPNAV_EVENT_ANY)
    assert m.spnav_remove_events.called

def test_spnav_poll_event_none():
    m = mock_libspnav({'spnav_poll_event' : 0 })
    assert spnav.spnav_poll_event() is None

def test_spnav_poll_event_motion():
    def motion(event):
        fill_motion_event(event)
        return 1
    m = mock_libspnav({'spnav_poll_event' : motion })
    event = spnav.spnav_poll_event()
    assert event is not None
    assert_equals(event.translation, (-1,2,-3))
    assert_equals(event.rotation, (10,-20,30))

def test_spnav_poll_event_button():
    def button(event):
        fill_button_event(event)
        return 1
    m = mock_libspnav({'spnav_poll_event' : button })
    event = spnav.spnav_poll_event()
    assert event is not None
    assert_equals(event.bnum, 0)
    assert_equals(event.press, True)

def test_spnav_wait_event_motion():
    def motion(event):
        fill_motion_event(event)
        return 1
    m = mock_libspnav({'spnav_wait_event' : motion })
    event = spnav.spnav_wait_event()
    assert event is not None
    assert_equals(event.translation, (-1,2,-3))
    assert_equals(event.rotation, (10,-20,30))

def test_spnav_wait_event_button():
    def button(event):
        fill_button_event(event)
        return 1
    m = mock_libspnav({'spnav_wait_event' : button })
    event = spnav.spnav_wait_event()
    assert event is not None
    assert_equals(event.bnum, 0)
    assert_equals(event.press, True)

@raises(spnav.SpnavWaitException)
def test_spnav_wait_event_fail():
    m = mock_libspnav({'spnav_wait_event' : 0 })
    spnav.spnav_wait_event()

