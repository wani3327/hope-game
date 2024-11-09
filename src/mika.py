import pygame
from pygame.locals import *
from helper import *
from pygame.math import Vector2
from bullet import *
from collider import *
from constants import *
from hog import Hog

BULLET_COOLDOWN = 300

class Mika:
    level_exp = [6,10,16,23,25,29,30,32,35,38,41,44,47,51]
    
    def __init__(self):
        self.image = pygame.image.load(r'resources\mika.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width() // 5, self.image.get_height() // 5))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.collider = CircleCollider(self, Vector2(0, 0), 30)
        self.speed = 0.5
        self.current_level = 1
        self.weapon_level = [0,0,0,0] # Bullet Fireball Lightning Bat
        self.cooldown = [[750,500,250],[3000,3000,3000],[5000,3000,3000],[3000,3000,3000]] # Bullet Fireball Lightning Bat
        self.bullet_cooldown = 0
        self.fireball_cooldown = 0
        self.lightning_cooldown = 0
        self.bat_cooldown = 0
        self.health = 100
        self.exp = 0
        

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
        
        if self.bullet_cooldown == 0:
            if hog_closest != None:
                position = self.collider.position.copy()

                b = Bullet(
                    position,
                    (hog_closest.collider.position - self.collider.position).normalize())
                bullets.append(b)
                space.add(b.collider)
                self.bullet_cooldown = self.cooldown[0][self.weapon_level[0]]
        else:
            self.bullet_cooldown -= 1
        
        if self.fireball_cooldown == 0:
                position = self.collider.position.copy()
                f = Fireball(position)
                bullets.append(f)
                space.add(f.collider)
                self.fireball_cooldown = self.cooldown[1][self.weapon_level[1]]
        else:
            self.fireball_cooldown -= 1
        
        if self.level_exp[self.current_level-1] <= self.exp:
            self.current_level += 1
            self.exp = 0
            

 
    def draw(self, surface, camera: Vector2):
        font = Font(None, 36)
        surface.blit(self.image, get_offset_camera(self.collider.position, camera, self.size))
        
        exp_text_obj = font.render(str(self.health), True, (0, 0, 0)) 
        exp_text_size =  Vector2(*exp_text_obj.get_rect().size)
        surface.blit(
            exp_text_obj, 
            get_offset_camera(
                self.collider.position + Vector2(0, 100),
                camera,
                exp_text_size
        ))

        exp_text_obj = font.render(str(self.exp), True, (0, 0, 0)) 
        exp_text_size = Vector2(*exp_text_obj.get_rect().size)
        surface.blit(
            exp_text_obj,
            get_offset_camera(
                self.collider.position + Vector2(0, 150),
                camera,
                exp_text_size
        ))

    def hit(self, amount: float) -> None:
        self.health -= amount

        if self.health <= 0:
            print('You died!')
            exit()