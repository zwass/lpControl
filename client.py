import logging
import socket

SOCKET_ADDR = ("localhost", 6666)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(SOCKET_ADDR)

print "Socket bound, waiting for data"

try:
    while True:
        data, addr = s.recvfrom(4)
        floatval = float(data.split("\n")[0])
        print floatval
except:
    logging.exception("recv loop %s", data)
finally:
    s.close()