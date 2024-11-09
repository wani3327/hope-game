import pygame
from pygame.locals import *
from helper import *
from pygame.math import Vector2
import bullet
from collider import *

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

    def update(self, bullets, space: PartitionedSpace):
        pressed_keys = pygame.key.get_pressed()
        mouse_pos = Vector2(*pygame.mouse.get_pos())

        if pressed_keys[K_UP]:
            movement = Vector2(0, -self.speed)
        if pressed_keys[K_DOWN]:
            movement = Vector2(0, self.speed)
        if pressed_keys[K_LEFT]:
            movement = Vector2(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            movement = Vector2(self.speed, 0)
        
        space.move(self.collider, self.collider.position + movement)

        if pressed_keys[K_SPACE]:
            if self.cooldown == 0:

                b = bullet.Bullet(
                        self.position.copy(), 
                        (mouse_pos - SCREEN_CENTER).normalize())
                bullets.append(b)
                space.add(b.collider)
                self.cooldown = BULLET_COOLDOWN
            else:
                self.cooldown -= 1
            

 
    def draw(self, surface, camera: Vector2):
        surface.blit(self.image, get_offset_camera(self.position, camera, self.size))

    def hit(self, amount: float) -> None:
        self.health -= amount

        if self.health <= 0:
            print('You died!')
            exit()