import pygame

class Spinner(pygame.sprite.Sprite):
    """
    Class for the spinner sprite.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('spinner_sprite.png')
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.orig_image = self.image

        self.rotation = 360.0

        self.loc = (120, 459) #correct location on phone

        self.next_update_time = 0

    #adapted from:
    #http://www.pygame.org/docs/ref/transform.html#pygame.transform.rotate
    def rotate(self, degrees):
        """
        Rotate the image sprite in place
        """
        orig_rect = self.orig_image.get_rect()
        self.image = pygame.transform.rotate(self.orig_image, degrees)
        rot_rect = orig_rect.copy()
        rot_rect.center = self.image.get_rect().center
        self.image = self.image.subsurface(rot_rect).copy()

    def update(self, degrees):
        self.rotation += degrees
        self.rotation = max(29.4, min(self.rotation, 360.0))
        print self.rotation
        self.rotate(self.rotation)
        # # Update every 10 milliseconds = 1/100th of a second.
        # if self.next_update_time < current_time:
        #     self.rotate(current_time / 10)
        #     #self.image = rot_center(self.orig_image, current_time / 10)
        #     self.next_update_time = current_time + 10