from globalvars import (STOPPED, FORWARD, FAST_FORWARD, REVERSE)

class StateMachine:

    def __init__(self):
        self.state = STOPPED
        self.prev = [0] * 10 #store 10 values

    def process(self, input):
        self.prev.pop()
        self.prev.insert(0, input)

        avg = sum(self.prev) / len(self.prev)

        if avg < 0:
            self.state = REVERSE
        elif avg == 0:
            self.state = STOPPED
        elif avg < 1.1:
            self.state = FORWARD
        else:
            self.state = FAST_FORWARD
        return self.state
