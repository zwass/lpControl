import logging
import socket


class StateMachine:
    STOPPED = 'STOPPED'
    FORWARD = 'FORWARD'
    FAST_FORWARD = 'FAST_FORWARD'
    REVERSE = 'REVERSE'

    def __init__(self):
        self.state = self.STOPPED
        self.prev = [0] * 10 #store 10 values

    def process(self, input):
        self.prev.pop()
        self.prev.insert(0, input)

        avg = sum(self.prev) / len(self.prev)

        if avg < 0:
            self.state = self.REVERSE
        elif avg == 0:
            self.state = self.STOPPED
        elif avg < 1.1:
            self.state = self.FORWARD
        else:
            self.state = self.FAST_FORWARD
        return self.state

SOCKET_ADDR = ("localhost", 6666)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(SOCKET_ADDR)

print "Socket bound, waiting for data"

state = StateMachine()

try:
    while True:
        data, addr = s.recvfrom(4)
        floatval = float(data.split("\n")[0])
        print floatval
        print state.process(floatval)
except:
    logging.exception("recv loop %s", data)
finally:
    s.close()
