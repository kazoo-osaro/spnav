import mock
import spnav
import ctypes

def mock_libspnav(methods):
    '''Replace spnav.libspnav with a mock object containing the supplied method
       names and return values.
       
       ``methods``: *dict*
          Dictionary mapping method names to return values.  If the return
          value is callable, then it will be called with the same arguments
          as the method and the return value from the callable will be used
          as the return value from the mock method.

       Returns: ``Mock`` object
    '''
    m = mock.Mock()
    for method, value in methods.items():
        mock_method = getattr(m, method)
        if callable(value):
            mock_method.side_effect = value
        else:
            mock_method.return_value = value
    spnav.libspnav = m
    return m

def fill_button_event(event_ref):
    event = event_ref.contents
    event.type = spnav.SPNAV_EVENT_BUTTON
    event.button.bnum = 0
    event.button.press = True

def fill_motion_event(event_ref):
    event = event_ref.contents
    event.type = spnav.SPNAV_EVENT_MOTION
    event.motion.x = -1
    event.motion.y = 2
    event.motion.z = -3
    event.motion.rx = 10
    event.motion.ry = -20
    event.motion.rz = 30
    event.motion.period = 0
