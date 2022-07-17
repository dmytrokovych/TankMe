import pygame
from pygame import Vector2
from settings import *
from math import sin, cos


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, status):

        if direction == Vector2(0, 0):
            direction = {'up':    Vector2(0, -1),
                         'down':  Vector2(0, 1),
                         'left':  Vector2(-1, 0),
                         'right': Vector2(1, 0),
                         'up_idle':    Vector2(0, -1),
                         'down_idle':  Vector2(0, 1),
                         'left_idle':  Vector2(-1, 0),
                         'right_idle': Vector2(1, 0)}
            self.direction = direction[status]
        else:
            self.direction = direction

        pos += self.direction * int(TILESIZE * 0.7)

        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)

        self.velocity = 10

    def update(self):
        self.rect.x += self.velocity * self.direction[0]
        self.rect.y += self.velocity * self.direction[1]
