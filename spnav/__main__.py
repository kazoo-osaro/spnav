from spnav import spnav_open, spnav_poll_event, spnav_close

if __name__ == '__main__':
    spnav_open()
    try:
        while True:
            event = spnav_poll_event()
            if event is not None:
                print event
    except KeyboardInterrupt:
        print '\nQuitting...'
    finally:
        spnav_close()

