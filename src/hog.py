import pygame
import random
from pygame.math import Vector2
from helper import *
import math

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
    image1 = pygame.image.load(r'resources\hog.png')
    size1 = Vector2(1, 1)
    image2 = pygame.image.load(r'resources\hog2.png')
    size2 = Vector2(1, 1)
    is_setup = False

    @classmethod
    def setup(cls):
        cls.image1 = pygame.transform.scale(cls.image1,
            (cls.image1.get_width() // 20, cls.image1.get_height() // 20))
        cls.size1 = Vector2(cls.image1.get_width(), cls.image1.get_height())
        cls.image2 = pygame.transform.scale(cls.image2,
            (cls.image2.get_width() // 20, cls.image2.get_height() // 20))
        cls.size2 = Vector2(cls.image2.get_width(), cls.image2.get_height())

    def __init__(self, level, mika_position):
        if not Hog.is_setup:
            self.setup()
            Hog.is_setup = True

        type = random.choices([0, 1, 2], weights=self.Hog_percentage[level])
        if type == [0]:
            self.image = 0
            self.speed = 0.2
            self.health = 1
            self.cooldown = 0
            self.power = 1
        elif type == [1]:
            self.image = 1
            self.speed = 0.2
            self.health = 11
            self.cooldown = 0
            self.power = 1
        else:
            self.image = 0
            self.speed = 0.2
            self.health = 21
            self.cooldown = 0
            self.power = 1

        
        x = random.randint(-600, 600)
        pos = mika_position + Vector2(x, int(math.sqrt(360000-x*x))*random.choice([-1,1]))
        self.collider = CircleCollider(self, pos, 20)
            
    def update(self, mika_currentposition, space: PartitionedSpace):
        space.move(self.collider, 
            self.collider.position + self.speed * Vector2.normalize(mika_currentposition - self.collider.position)
        )

        if self.cooldown != 0:
            self.cooldown -= 1
 
    def draw(self, surface, camera):

        if self.image == 0:
            surface.blit(
                Hog.image1, 
                get_offset_camera(self.collider.position, camera, Hog.size1))
        else:
            surface.blit(
                Hog.image2,
                get_offset_camera(self.collider.position, camera, Hog.size2))
        

    def hit(self, amount) -> bool:
        self.health -= amount
        return self.health <= 0
    
    def attack(self) -> float:
        if self.cooldown == 0:
            self.cooldown = HOG1_ATTACK_COOLDOWN
            return self.power
        return 0
