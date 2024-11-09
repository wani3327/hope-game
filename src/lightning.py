import pygame
from pygame.math import Vector2
from helper import *
from collider import CircleCollider, PartitionedSpace
from hog import Hog


class Lightning:
    def __init__(self, initial_position: Vector2):
        # print('bullet', initial_position, direction)
        self.image = pygame.image.load(r'resources\lightning.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 70, self.image.get_height() // 70))
        self.position = initial_position
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.lifetime = 100
    
    def update(self):#, space: PartitionedSpace):
        self.lifetime -= 1

    def draw(self, surface, camera: Vector2):
        surface.blit(self.image, get_offset_camera(self.position, camera, self.size))