import pygame
from pygame.locals import *
from helper import *
from pygame.math import Vector2
from bullet import *
from collider import *
from constants import *
from hog import Hog
from orb import Drop, Item
from pygame.surface import Surface

BULLET_COOLDOWN = 60

class Mika:
    level_exp = [6,10,16,23,25,29,30,32,35,38,41,44,47,51]
    
    def __init__(self):
        self.image: list[Surface] = []

        for i in range(4):
            img = pygame.image.load(rf'resources\Eilin\move{i}.png')
            img = pygame.transform.scale(img, 
                (img.get_width() // 0.7, img.get_height() // 0.7))
            self.image.append(img)

        self.size = Vector2(self.image[0].get_width(), self.image[0].get_height())
        self.collider = CircleCollider(self, Vector2(0, 0), 30)
        self.sprite_clock = 0
        
        self.speed = 3
        self.current_level = 1
        self.health = 100
        self.exp = 0
        self.looking_left = False

        # weapon
        self.weapon_level = [0, -1, -1, -1] # Bullet Fireball Lightning Bat
        self.cooldown = [[45,30,15],[180,180,180],[300,180,180],[3000,3000,3000]] # Bullet Fireball Lightning Bat
        self.bullet_cooldown = 0
        self.fireball_cooldown = 0
        self.lightning_cooldown = 0
        self.bat_cooldown = 0
        
    def update(self, bullets: set[Bullet], lightnings:set[Lightning], hog_list:set[Hog]):
        pressed_keys = pygame.key.get_pressed()
        movement = Vector2(0, 0)

        if pressed_keys[K_UP]:
            movement += Vector2(0, -self.speed)
        if pressed_keys[K_DOWN]:
            movement += Vector2(0, self.speed)
        if pressed_keys[K_LEFT]:
            if not self.looking_left:
                self.looking_left = True
                self.flip()
            movement += Vector2(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            if self.looking_left:
                self.looking_left = False
                self.flip()
            movement += Vector2(self.speed, 0)
        
        if movement.length_squared() != 0:
            self.sprite_clock += 1

        self.collider.position += movement

        
        
        if self.weapon_level[0] >= 0:    
            if self.bullet_cooldown == 0:
                closest_hog = self.find_nearest(hog_list)
                if closest_hog != None:
                    position = self.collider.position.copy()
                    b = Bullet(
                        position,
                        (closest_hog.collider.position - self.collider.position).normalize(),
                        damage=6)
                    bullets.add(b)
                    self.bullet_cooldown = self.cooldown[0][self.weapon_level[0]]
            else:
                self.bullet_cooldown -= 1
        
        if self.weapon_level[1] >= 0:
            if self.fireball_cooldown == 0:
                position = self.collider.position.copy()
                f = Fireball(position,damage=11)
                bullets.add(f)
                self.fireball_cooldown = 750
            else:
                self.fireball_cooldown -= 1
    
        if self.weapon_level[2] >= 0:
            if self.lightning_cooldown == 0:
                if len(hog_list) >= 1:
                    if self.weapon_level[2] == 2 and len(hog_list) >= 2:
                        hog_lightning_list = random.sample(list(hog_list), 2)
                        position = hog_lightning_list[0].collider.position.copy()
                        l = Lightning(position,damage=20)
                        lightnings.add(l)
                        position = hog_lightning_list[1].collider.position.copy()
                        l = Lightning(position,damage=20)
                        lightnings.add(l)
                        self.lightning_cooldown = self.cooldown[2][self.weapon_level[2]]
                    else:
                        hog_lightning_list = random.choice(list(hog_list))
                        position = hog_lightning_list.collider.position.copy()
                        l = Lightning(position,damage=20)
                        lightnings.add(l)
                        self.lightning_cooldown = self.cooldown[2][self.weapon_level[2]]
            else:
                self.lightning_cooldown -= 1
                
    
    def flip(self):
        n = []
        for i in self.image:
            n.append(pygame.transform.flip(i, True, False))
        self.image = n

    def find_nearest(self, hog_list: list[Hog]):
        closest_hog = None
        min_distance = 999999
        for h in hog_list:
            d = Vector2.magnitude(h.collider.position - self.collider.position)
            if d < min_distance:
                min_distance = d
                closest_hog = h
        return closest_hog

        
        
    def try_level_up(self, get_exp_value: int, space: PartitionedSpace, orb_set: set[Drop]):
        self.exp += get_exp_value
        items = []
        
        if self.level_exp[self.current_level-1] <= self.exp:
            self.current_level += 1
            self.exp = 0
            for i in range(3):
                r = random.randint(0, 2)
                v = ['bow', 'fireball', 'lightning'][r]
                item = Item(self.collider.position + Vector2(200 * i - 200, 200), v)
                items.append(item)
                orb_set.add(item)
                space.add(item.collider)

        for i in items:
            i.friend = items

    def get_item(self, item: Item):
        if item.value == 'bow' and self.weapon_level[0] < 2:
            self.weapon_level[0] += 1
        elif item.value == 'fireball' and self.weapon_level[1] < 2:
            self.weapon_level[1] += 1
        elif item.value == 'lightning' and self.weapon_level[2] < 2:
            self.weapon_level[2] += 1

 
    def draw(self, surface, camera: Vector2):

        surface.blit(self.image[(self.sprite_clock // 15) % 4], 
            get_offset_camera(self.collider.position, camera, self.size))
        
        font = Font(None, 36)
        
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
                self.collider.position + Vector2(0, 130),
                camera,
                exp_text_size
        ))

        item_text_obj = font.render(str(self.weapon_level), True, (0, 0, 0))
        item_text_size = Vector2(*item_text_obj.get_rect().size)
        surface.blit(
            item_text_obj,
            get_offset_camera(
                self.collider.position + Vector2(0, 160),
                camera,
                item_text_size
        ))


    def hit(self, amount: float) -> None:
        self.health -= amount

        if self.health <= 0:
            print('You died!')
            exit()