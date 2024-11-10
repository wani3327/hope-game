import pygame
from pygame.math import Vector2
from helper import *
from collider import CircleCollider, PartitionedSpace
import math
import random

class Bullet:
    def __init__(self, initial_position: Vector2, direction: Vector2, damage):
        # print('bullet', initial_position, direction)
        self.image = pygame.image.load(r'resources\bat.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 7, self.image.get_height() // 7))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.direction = direction
        self.speed = 5
        self.collider = CircleCollider(self, initial_position, 20)
        self.lifetime = 10
        self.damage = damage
    
    def update(self, mika_current_position):#, space: PartitionedSpace):
        self.collider.position = mika_current_position
        # space.move(self.collider, self.collider.position + self.speed * self.direction)
        self.lifetime -= 1

    def draw(self, surface, camera: Vector2):
        surface.blit(self.image, get_offset_camera(self.collider.position, camera, self.size))