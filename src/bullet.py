import pygame
from pygame.math import Vector2
from helper import *

class Bullet:
    def __init__(self, initial_position: Vector2, direction: Vector2):
        print('bullet', initial_position, direction)
        self.image = pygame.image.load(r'resources\hots.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width(), self.image.get_height()))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.position = initial_position
        self.direction = direction
        self.speed = 5
    
    def update(self):
        self.position += self.speed * self.direction

    def draw(self, surface, camera: Vector2):
        surface.blit(self.image, get_offset_camera(self.position, camera, self.size))