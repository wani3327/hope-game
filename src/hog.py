import pygame
import random
from pygame.math import Vector2
from helper import *

from pygame.locals import *
from collider import CircleCollider, PartitionedSpace

class Hog:
    def __init__(self, mika_position):
        self.image = pygame.image.load(r'resources\hog.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//50, self.image.get_height()//50))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        pos = Vector2(random.randint(0,600), random.randint(0, 300))
        self.collider = CircleCollider(self, pos, 20)
        self.mika_position = mika_position
        self.velocity = 0.2

    def update(self, space: PartitionedSpace):
        space.move(self.collider, 
            self.collider.position + self.velocity * Vector2.normalize(self.mika_position - self.collider.position)
        )
 
    def draw(self, surface, camera):
        surface.blit(self.image, get_offset_camera(self.collider.position, camera, self.size))

    def hit(self, amount):
        print("got hit", amount)
