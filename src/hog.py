import pygame
import random
from pygame.math import Vector2
from helper import *

from pygame.locals import *
from collider import CircleCollider, PartitionedSpace

HOG1_ATTACK_COOLDOWN = 15

class Hog:
    Hog_percentage = {
        1:[1,0,0],
        2:[0.9,0.1,0],
        3:[0.8,0.2,0],
        4:[0.7,0.3,0],
        5:[0.6,0.4,0],
        6:[0.5,0.4,0.1],
        7:[0.4,0.5,0.1],
        8:[0.4,0.4,0.2],
        9:[0.3,0.5,0.2],
        10:[0.3,0.4,0.3],
        11:[0.2,0.5,0.3],
        12:[0.2,0.4,0.2],
        13:[0.1,0.4,0.5],
        14:[0,0.4,0.6]
    }
    def __init__(self, level, mika_position):
        print(self.Hog_percentage[3])
        type = random.choices(range(0,3), weights=self.Hog_percentage[level])
        if type == 0:
            self.image = pygame.image.load(r'resources\hog.png')
            self.speed = 0.2
            self.health = 1
            self.cooldown = 0
            self.power = 1
        elif type == 1:
            self.image = pygame.image.load(r'resources\hog.png')
            self.speed = 0.2
            self.health = 11
            self.cooldown = 0
            self.power = 1
        else:
            self.image = pygame.image.load(r'resources\hog.png')
            self.speed = 0.2
            self.health = 21
            self.cooldown = 0
            self.power = 1

        self.image = pygame.transform.scale(self.image, (self.image.get_width()//20, self.image.get_height()//20))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        pos = Vector2(random.randint(0, 600), random.randint(0, 300))
        self.collider = CircleCollider(self, pos, 20)
        self.mika_position = mika_position
            
            # status
            
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
