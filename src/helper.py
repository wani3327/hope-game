import pygame
from constants import *

screen = pygame.math.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)

def get_offset_camera(position: pygame.math.Vector2, camera: pygame.math.Vector2, size: pygame.math.Vector2):
    offset = position - camera + screen / 2 - size / 2
    return pygame.Rect(offset.x, offset.y, size.x, size.y)