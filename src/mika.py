import pygame
from pygame.locals import *
from helper import *
from pygame.math import Vector2
import bullet

class Mika:
    def __init__(self):
        self.image = pygame.image.load(r'resources\mika.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 5, self.image.get_height() // 5))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.position = Vector2(0, 0)
        self.speed = 0.5
        self.cooldown = 0

    def update(self, bullets, space):
        pressed_keys = pygame.key.get_pressed()
        mouse_pos = Vector2(*pygame.mouse.get_pos())

        if pressed_keys[K_UP]:
            self.position += Vector2(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.position += Vector2(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.position += Vector2(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.position += Vector2(self.speed, 0)
        
        if pressed_keys[K_SPACE]:
            if self.cooldown == 0:

                b = bullet.Bullet(
                        self.position.copy(), 
                        (mouse_pos - SCREEN_CENTER).normalize())
                bullets.append(b)
                space.add(b.collider)
                self.cooldown = 60
            else:
                self.cooldown -= 1
            

 
    def draw(self, surface, camera: Vector2):
        surface.blit(self.image, get_offset_camera(self.position, camera, self.size))