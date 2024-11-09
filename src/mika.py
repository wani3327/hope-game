import pygame
from pygame.locals import *
from helper import *
from pygame.math import Vector2
import bullet
from collider import *
from constants import *
from hog import Hog

BULLET_COOLDOWN = 300

class Mika:
    def __init__(self):
        self.image = pygame.image.load(r'resources\mika.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 5, self.image.get_height() // 5))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.collider = CircleCollider(self, Vector2(0, 0), 20)
        self.speed = 0.5
        self.cooldown = 0
        self.health = 100

    def update(self, bullets, space: PartitionedSpace, hog_closest: Hog | None =None):
        pressed_keys = pygame.key.get_pressed()
        movement = Vector2(0, 0)

        if pressed_keys[K_UP]:
            movement = Vector2(0, -self.speed)
        if pressed_keys[K_DOWN]:
            movement = Vector2(0, self.speed)
        if pressed_keys[K_LEFT]:
            movement = Vector2(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            movement = Vector2(self.speed, 0)
        
        space.move(self.collider,
                   self.collider.position + movement)
        
        if self.cooldown == 0:
            if hog_closest != None:
                b = bullet.Bullet(
                        self.collider.position.copy(), 
                        (hog_closest.collider.position - self.collider.position).normalize())
                bullets.append(b)
                space.add(b.collider)
                self.cooldown = 750
        else:
            self.cooldown -= 1
            

 
    def draw(self, surface, camera: Vector2):
        font = Font(None, 36)
        surface.blit(self.image, get_offset_camera(self.collider.position, camera, self.size))
        text_obj = font.render(str(self.health), True, (0, 0, 0)) 
        text_size =  Vector2(*text_obj.get_rect().size)
        surface.blit(
            text_obj, 
            get_offset_camera(
                self.collider.position + Vector2(0, 100),
                camera,
                text_size
        ))

    def hit(self, amount: float) -> None:
        self.health -= amount

        if self.health <= 0:
            print('You died!')
            exit()