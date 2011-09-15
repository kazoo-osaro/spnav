from spnav import *
spnav_open()
try:
    while True:
        ev = spnav_poll_event()
        if ev is not None:
            print ev
except KeyboardInterrupt:
    print '\nQuitting...'
finally:
    spnav_close()

