from nose.tools import raises
import spnav

def test_spnav_motion_str():
    event = spnav.SpnavMotionEvent((-1,-2,-3), (10, 20, 30), 0)
    s = str(event)
    assert 'MOTION' in s
    assert '-1' in s
    assert '20' in s

def test_spnav_button_down_str():
    event = spnav.SpnavButtonEvent(1, True)
    s = str(event)
    assert 'BUTTON' in s
    assert '1' in s
    assert 'down'

def test_spnav_button_up_str():
    event = spnav.SpnavButtonEvent(1, False)
    s = str(event)
    assert 'BUTTON' in s
    assert '1' in s
    assert 'up'

@raises(spnav.SpnavException)
def test_convert_spnav_event_fail():
    c_event = spnav.spnav_event()
    c_event.type = spnav.SPNAV_EVENT_ANY # not allowed
    spnav.convert_spnav_event(c_event)
