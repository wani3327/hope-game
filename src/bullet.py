import pygame
from pygame.math import Vector2
from helper import *

class Bullet:
    def __init__(self, initial_position: Vector2, momentum: Vector2):
        self.image = pygame.image.load(r'resources\mika.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 5, self.image.get_height() // 5))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.position = initial_position
        self.momentum = momentum
        self.speed = 0.5
    
    def update(self):
        self.position += self.speed * self.momentum

    def draw(self, surface, camera: Vector2):
        surface.blit(self.image, get_offset_camera(self.position, camera, self.size))