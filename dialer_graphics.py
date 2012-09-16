import pygame
import pygame.image
from pygame.locals import *

from spinner import Spinner

# With help from:
#http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml

pygame.init()
screen = pygame.display.set_mode([531, 800])
bg = pygame.image.load('phone_sprite.png')

spinner = Spinner()

needle = pygame.image.load('needle_sprite.png')
needle.set_colorkey(needle.get_at((0,0)))


while pygame.event.poll().type != KEYDOWN:
    screen.fill([0, 0, 0]) # blank the screen.

    spinner.update(pygame.time.get_ticks())

    screen.blit(bg, bg.get_rect())
    screen.blit(spinner.image, spinner.loc, spinner.image.get_rect())
    screen.blit(needle, needle.get_rect())
    pygame.display.update()
