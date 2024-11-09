from pygame.math import Vector2
from collider import *
from helper import *

class Drop:
    def __init__(self) -> None:
        pass

    def draw(self, surface, camera):
        surface.blit(self.image, get_offset_camera(self.collider.position, camera, self.size))


class ExpOrb(Drop):
    def __init__(self, position: Vector2, value: int) -> None:
        self.image = pygame.image.load(r'resources\diamond.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//20, self.image.get_height()//20))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.value = value
        self.collider = CircleCollider(self, position, 10)
                
    
class Item(Drop):
    def __init__(self, position: Vector2, value: str) -> None:
        self.value = value
        path = ''
        scale = 1

        if value == 'bow':
            path = 'hots'
            scale = 5
        elif value == 'fireball':
            path = 'fireball'
            scale = 5
        elif value == 'lightning':
            path = 'lightning'
            scale = 50

        self.image = pygame.image.load(fr'resources\{path}.png')
        self.image = pygame.transform.scale(self.image, 
            (self.image.get_width()//scale, self.image.get_height()//scale))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.value = value
        self.collider = CircleCollider(self, position, 10)