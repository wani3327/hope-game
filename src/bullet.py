import pygame
from pygame.math import Vector2
from helper import *
from collider import CircleCollider, PartitionedSpace
import math
import random

class Bullet:
    def __init__(self, initial_position: Vector2, direction: Vector2, damage):
        # print('bullet', initial_position, direction)
        self.image = pygame.image.load(r'resources\hots.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 7, self.image.get_height() // 7))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.direction = direction
        self.speed = 5
        self.collider = CircleCollider(self, initial_position, 10)
        self.lifetime = 300
        self.damage = damage
    
    def update(self):#, space: PartitionedSpace):
        self.collider.position = self.collider.position + self.speed * self.direction
        # space.move(self.collider, self.collider.position + self.speed * self.direction)
        self.lifetime -= 1

    def draw(self, surface, camera: Vector2):
        surface.blit(self.image, get_offset_camera(self.collider.position, camera, self.size))


class Fireball(Bullet):
    def __init__(self, initial_position: Vector2, damage):
        self.image = pygame.image.load(r'resources\fireball.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 7, self.image.get_height() // 7))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        angle = random.random() * 2 * math.pi
        self.direction = Vector2(math.cos(angle), math.sin(angle))
        self.speed = 4
        self.collider = CircleCollider(self, initial_position, 10)
        self.lifetime = 300
        self.damage = damage
    
    def update(self):
        self.collider.position += self.speed * self.direction
=========
    def update(self):#, space: PartitionedSpace):
        self.collider.position = self.collider.position + self.speed * self.direction
        # space.move(self.collider, self.collider.position + self.speed * self.direction)
>>>>>>>>> Temporary merge branch 2
        self.lifetime -= 1

class Lightning(Bullet):
    def __init__(self, initial_position: Vector2, damage):
        self.image = pygame.image.load(r'resources\lightning.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 50, self.image.get_height() // 50))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.collider = CircleCollider(self, initial_position, 50)
        self.lifetime = 300
        self.damage = damage
        self.used = False
    
    def update(self):
        self.lifetime -= 1