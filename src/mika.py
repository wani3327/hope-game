import pygame
from pygame.locals import *
from helper import *
from pygame.math import Vector2
from bullet import *
from collider import *
from constants import *
from hog import Hog
from orb import Drop, Item

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
        
        self.bullet_available = True
        self.bullet_cooldown = 0
        self.fireball_available = False
        self.fireball_cooldown = 0

    def update(self, bullets, spaces: list[PartitionedSpace], hog_closest: Hog | None =None):
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
        
        self.collider.position += movement
        

        if self.bullet_available:    
            if self.bullet_cooldown == 0:
                if hog_closest != None:
                    position = self.collider.position.copy()
                    b = Bullet(
                        position,
                        (hog_closest.collider.position - self.collider.position).normalize())
                    bullets.add(b)
                    self.bullet_cooldown = 750
            else:
                self.bullet_cooldown -= 1
        
        if self.fireball_available:
            if self.fireball_cooldown == 0:
                position = self.collider.position.copy()
                f = Fireball(position)
                bullets.add(f)
                self.fireball_cooldown = 750
            else:
                self.fireball_cooldown -= 1
        
        
        
    def try_level_up(self, get_exp_value: int, space: PartitionedSpace, orb_set: set[Drop]):
        self.exp += get_exp_value

        if self.level_exp[self.current_level-1] <= self.exp:
            self.current_level += 1
            self.exp = 0

        for i in range(3):
            r = random.randint(0, 2)
            v = ['bow', 'fireball', 'lightning'][r]
            item = Item(self.collider.position + Vector2(200 * i - 200, 200), v)
            orb_set.add(item)
            space.add(item.collider)

 
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