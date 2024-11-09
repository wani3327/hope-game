import pygame
import random
from pygame.math import Vector2
from helper import *

from pygame.locals import *

class Hog:
    def __init__(self, mika_position):
        self.mika_position = mika_position
        self.velocity = 0.2
        self.image = pygame.image.load(r'resources\hog.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//50, self.image.get_height()//50))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.position = Vector2(random.randint(0,600), random.randint(0, 300)) + self.mika_position
        # self.rect.scale_by_ip(0.1, 0.1)

    def update(self):
        self.position += self.velocity*pygame.math.Vector2.normalize(self.mika_position - self.position)
 
    def draw(self, surface, camera):
        surface.blit(self.image, get_offset_camera(self.position, camera, self.size))