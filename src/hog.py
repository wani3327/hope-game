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
    image1: list[pygame.surface.Surface] = []
    image1v: list[pygame.surface.Surface] = []
    size1 = Vector2(1, 1)
    image2: list[pygame.surface.Surface] = []
    image2v: list[pygame.surface.Surface] = []
    size2 = Vector2(1, 1)
    is_setup = False

    @classmethod
    def setup(cls):
        for i in range(4):
            img = pygame.image.load(fr'resources\Warhog\hog{i}.png')
            img = pygame.transform.scale(img,
                (img.get_width() // 0.5, img.get_height() // 0.5))
            cls.image1.append(img)
            cls.image1v.append(pygame.transform.flip(img, True, False))

        cls.size1 = Vector2(cls.image1[0].get_width(), cls.image1[0].get_height())

        for i in range(4):
            img = pygame.image.load(fr'resources\hog2.png')
            img = pygame.transform.scale(img,
                (img.get_width() // 17, img.get_height() // 17))
            cls.image2.append(img)
            cls.image2v.append(pygame.transform.flip(img, True, False))

        cls.size2 = Vector2(cls.image2[0].get_width(), cls.image2[0].get_height())

    def __init__(self, level, mika_position):
        if not Hog.is_setup:
            self.setup()
            Hog.is_setup = True

        type = random.choices([0, 1, 2], weights=self.Hog_percentage[level])
        if type == [0]:
            self.image = 0
            self.speed = 1.2
            self.health = 1
            self.cooldown = 0
            self.power = 1
        elif type == [1]:
            self.image = 1
            self.speed = 1.8
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
        self.collider = CircleCollider(self, pos, 30)
        self.sprite_clock = 0
        self.looking_left = False
        self.dash_cooldown = 0
            
    def update(self, mika_currentposition: Vector2, space: PartitionedSpace):
        dashing = False

        if self.dash_cooldown != 0:
            self.dash_cooldown -= 1

        if self.image == 1:
            d = mika_currentposition.distance_squared_to(self.collider.position)
            if d < 40000 and self.dash_cooldown == 0:
                dashing = True
            if d < 4000:
                self.dash_cooldown = 300
                dashing = False


        new_pos = self.collider.position \
            + self.speed * Vector2.normalize(mika_currentposition - self.collider.position)

        collision = space.do_collide(CircleCollider(self, new_pos, 60))
        
        if collision != None and type(collision.object) is Hog:
            distance_btw_colliding_hog = collision.position.distance_squared_to(self.collider.position)
            if 0 < distance_btw_colliding_hog:
                opposite_direction = (self.collider.position - collision.position).normalize()
                new_pos = self.collider.position + self.speed * opposite_direction
            else:
                new_pos = self.collider.position + Vector2(1, 0)
            self.dash_cooldown = 300
            dashing = False


        if (not self.looking_left) and (mika_currentposition - self.collider.position).x < 0:
            self.looking_left = True
        elif self.looking_left and (mika_currentposition - self.collider.position).x > 0:
            self.looking_left = False

        if dashing:
            new_pos = (new_pos - self.collider.position) * 10 + self.collider.position
        space.move(self.collider, new_pos)

        self.sprite_clock += 1
        if self.cooldown != 0:
            self.cooldown -= 1
 
    def draw(self, surface, camera):
        index = (self.sprite_clock // 15) % 4
        sprites = None
        size = Vector2(1, 1)

        if self.image == 0:
            size = self.size1
            if self.looking_left:
                sprites = Hog.image1v
            else:
                sprites = Hog.image1
        else:
            size = self.size2
            if self.looking_left:
                sprites = Hog.image2v
            else:
                sprites = Hog.image2

        surface.blit(
            sprites[index],
            get_offset_camera(self.collider.position, camera, size))
        

    def hit(self, amount) -> bool:
        self.health -= amount
        print(f'hog hurts {amount} => {self.health}')
        return self.health <= 0
    
    def attack(self) -> float:
        if self.cooldown == 0:
            self.cooldown = HOG1_ATTACK_COOLDOWN
            return self.power
        return 0
