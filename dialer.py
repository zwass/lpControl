import logging
import socket
from time import time

import pygame
from pygame.locals import KEYDOWN

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

# PyGame help from:
#http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SOCKET_ADDR)

sm = StateMachine()
state = sm.state


pygame.init()
screen = pygame.display.set_mode([531, 800])
bg = pygame.image.load('phone_sprite.png')

spinner = Spinner()

needle = pygame.image.load('needle_sprite.png')
needle.set_colorkey(needle.get_at((0,0)))

try:
    while pygame.event.poll().type != KEYDOWN:
        data, addr = sock.recvfrom(4)
        floatval = float(data.split("\n")[0])
        sm.process(floatval)

        spinner.update(floatval * degrees_per_sample)

        screen.fill([0, 0, 0]) # blank the screen.
        screen.blit(bg, bg.get_rect())
        screen.blit(spinner.image, spinner.loc, spinner.image.get_rect())
        screen.blit(needle, needle.get_rect())
        pygame.display.update()


        # new_state = sm.state
        # if state in (REVERSE, STOPPED):
        #     if new_state == REVERSE:
        #         vel_sum += floatval
        #     elif new_state == STOPPED:
        #         vel_ # WAT?
        # if state != FORWARD and new_state == FORWARD:
        #     pass
        # elif state != STOPPED and new_state == STOPPED:
        #     pass
        # elif state != REVERSE and new_state == REVERSE:
        #     start_time = time()
        #     vel_sum = floatval
        # elif state != FAST_FORWARD and new_state == FAST_FORWARD:
        #     pass

        # state = new_state

except:
    logging.exception("recv loop")
finally:
    sock.close()
