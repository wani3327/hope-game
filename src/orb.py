from pygame.math import Vector2
from collider import *
from helper import *


class ExpOrb:
    def __init__(self, position: Vector2, value: int) -> None:
        self.image = pygame.image.load(r'resources\diamond.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()//20, self.image.get_height()//20))
        self.size = Vector2(self.image.get_width(), self.image.get_height())
        self.value = value
        self.collider = CircleCollider(self, position, 10)

                
    def draw(self, surface, camera):
        surface.blit(self.image, get_offset_camera(self.collider.position, camera, self.size))