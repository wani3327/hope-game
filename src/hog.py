import pygame
import random
from pygame.math import Vector2
from helper import *

from pygame.locals import *
from collider import CircleCollider, PartitionedSpace

HOG1_ATTACK_COOLDOWN = 15

class Hog:
    def __init__(self, mika_position):
        self.image = pygame.image.load(r'resources\hog.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//50, self.image.get_height()//50))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        pos = Vector2(random.randint(0,600), random.randint(0, 300))
        self.collider = CircleCollider(self, pos, 20)
        self.mika_position = mika_position
        
        # status
        self.speed = 0.2
        self.health = 1
        self.cooldown = 0
        self.power = 1

    def update(self, space: PartitionedSpace):
        space.move(self.collider, 
            self.collider.position + self.speed * Vector2.normalize(self.mika_position - self.collider.position)
        )

        if self.cooldown != 0:
            self.cooldown -= 1
 
    def draw(self, surface, camera):
        surface.blit(self.image, get_offset_camera(self.collider.position, camera, self.size))

    def hit(self, amount) -> bool:
        self.health -= amount
        return self.health <= 0
    
    def attack(self) -> float:
        if self.cooldown == 0:
            self.cooldown = HOG1_ATTACK_COOLDOWN
            return self.power
        return 0
