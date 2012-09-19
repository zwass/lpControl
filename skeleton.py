import logging
import socket

from globalvars import (SOCKET_ADDR, STOPPED, FORWARD, FAST_FORWARD, REVERSE)
from statemachine import StateMachine

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SOCKET_ADDR)

print "Socket bound, waiting for data"

sm = StateMachine()
try:
    while True:
        data, addr = sock.recvfrom(4)
        floatval = float(data.split("\n")[0])
        print sm.process(floatval)
except:
    logging.exception("recv loop %s", data)
finally:
    sock.close()
