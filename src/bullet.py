import pygame
from pygame.math import Vector2
from helper import *
from collider import CircleCollider, PartitionedSpace


class Bullet:
    def __init__(self, initial_position: Vector2, direction: Vector2):
        # print('bullet', initial_position, direction)
        self.image = pygame.image.load(r'resources\hots.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 7, self.image.get_height() // 7))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.direction = direction
        self.speed = 5
        self.collider = CircleCollider(self, initial_position, 10)
        self.lifetime = 300
    
    def update(self):#, space: PartitionedSpace):
        self.collider.position = self.collider.position + self.speed * self.direction
        # space.move(self.collider, self.collider.position + self.speed * self.direction)
        self.lifetime -= 1

        if self.lifetime == 0:
            # we will take care of this situation in App
            pass

    def draw(self, surface, camera: Vector2):
        surface.blit(self.image, get_offset_camera(self.collider.position, camera, self.size))

import pygame
from pygame.math import Vector2
from helper import *
from collider import CircleCollider, PartitionedSpace
import math
import random
from bullet import Bullet

class Fireball(Bullet):
    def __init__(self, initial_position: Vector2):
        self.image = pygame.image.load(r'resources\fireball.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 7, self.image.get_height() // 7))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        angle = random.random() * 2 * math.pi
        self.direction = Vector2(math.cos(angle), math.sin(angle))
        self.speed = 4
        self.collider = CircleCollider(self, initial_position, 10)
        self.lifetime = 300
    
    def update(self):
        self.collider.position += self.speed * self.direction
        self.lifetime -= 1

        if self.lifetime == 0:
            # we will take care of this situation in App
            pass
