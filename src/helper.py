import pygame
from constants import *


def get_offset_camera(position: pygame.math.Vector2, camera: pygame.math.Vector2, size: pygame.math.Vector2):
    offset = position - camera + SCREEN_CENTER - size / 2
    return pygame.Rect(offset.x, offset.y, size.x, size.y)