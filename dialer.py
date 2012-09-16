import logging
import socket
import time
import sys

import pygame
from pygame.locals import KEYDOWN
from twilio.rest import TwilioRestClient

from spinner import Spinner


from globalvars import(SOCKET_ADDR, STOPPED,
                       FORWARD, FAST_FORWARD, REVERSE,
                       SAMPLES_PER_SECOND)
from statemachine import StateMachine

SECONDS_PER_REVOLUTION = 60.0 / 33 #33 RPM
REVOLUTIONS_PER_SECOND = 33 / 60.0

FULL_REVOLUTION_INTEGRAL = SECONDS_PER_REVOLUTION * 1.0

seconds_per_sample = 1.0 / SAMPLES_PER_SECOND
degrees_per_second = 360 * REVOLUTIONS_PER_SECOND
degrees_per_sample = degrees_per_second * seconds_per_sample


def detect_number(angle):
    """
    Return the dialed number based on the minimum rotation achieved.

    Starting at 360 degrees, we subtract the rotation.
    These values were determined by observation.
    """
    if angle < 32:
        return 0
    elif angle < 63:
        return 9
    elif angle < 94:
        return 8
    elif angle < 125:
        return 7
    elif angle < 154:
        return 6
    elif angle < 184:
        return 5
    elif angle < 215:
        return 4
    elif angle < 246:
        return 3
    elif angle < 275:
        return 2
    elif angle < 304:
        return 1
    else:
        return None

# PyGame help from:
#http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SOCKET_ADDR)

sm = StateMachine()
state = sm.state


pygame.init()
pygame.display.set_caption("lpDialer")
screen = pygame.display.set_mode([531, 800])
bg = pygame.image.load('phone_sprite.png')

spinner = Spinner()

needle = pygame.image.load('needle_sprite.png')
needle.set_colorkey(needle.get_at((0,0)))

last_time = time.time()

number_string = ""

try:
    while pygame.event.poll().type != KEYDOWN and len(number_string) < 10:
        data, addr = sock.recvfrom(4)

        cur_time = time.time()
        time_delta = cur_time - last_time
        last_time = cur_time

        multiplier = time_delta / seconds_per_sample

        floatval = float(data.split("\n")[0])
        sm.process(floatval)

        spinner.update(floatval * degrees_per_sample * multiplier)

        if abs(360.0 - spinner.rotation) < .01:
            dialed_number = detect_number(spinner.min_rotation)
            if dialed_number is not None:
                number_string += str(dialed_number)
                if len(number_string) == 1:
                    sys.stdout.write("(%d" % dialed_number)
                elif len(number_string) == 2:
                    sys.stdout.write(str(dialed_number))
                elif len(number_string) == 3:
                    sys.stdout.write("%d) " % dialed_number)
                elif len(number_string) <= 6:
                    sys.stdout.write(str(dialed_number))
                elif len(number_string) == 7:
                    sys.stdout.write("-%d" % dialed_number)
                else:
                    sys.stdout.write(str(dialed_number))
                sys.stdout.flush()
            spinner.min_rotation = 360.0

        screen.fill([0, 0, 0]) # blank the screen.
        screen.blit(bg, bg.get_rect())
        screen.blit(spinner.image, spinner.loc, spinner.image.get_rect())
        screen.blit(needle, needle.get_rect())
        pygame.display.update()

except:
    logging.exception("recv loop")
finally:
    sock.close()

if len(number_string) == 10:
    try:
        client = TwilioRestClient()
        call = client.calls.create(to=number_string,
                                   from_="8653831234",
                                   url="http://demo.brooklynhacker.com/amit.xml")
    except:
        pass
    print
    print "Calling..."
    pygame.time.wait(30 * 1000)
