import logging
import socket

import spotifycontrol as spotify

from globalvars import (SOCKET_ADDR, STOPPED, FORWARD, FAST_FORWARD, REVERSE)
from statemachine import StateMachine

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SOCKET_ADDR)

print "Socket bound, waiting for data"

sm = StateMachine()
state = sm.state

try:
    while True:
        data, addr = sock.recvfrom(4)
        floatval = float(data.split("\n")[0])
        print sm.process(floatval)
        new_state = sm.state
        if state == STOPPED and new_state == FORWARD:
            spotify.play()
        elif state != STOPPED and new_state == STOPPED:
            spotify.pause()
        elif state != REVERSE and new_state == REVERSE:
            spotify.prev()
        elif state != FAST_FORWARD and new_state == FAST_FORWARD:
            spotify.next()
        state = new_state
except:
    logging.exception("recv loop %s", data)
finally:
    sock.close()
