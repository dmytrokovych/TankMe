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

        self.velocity = 10

        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        self.rect.x += self.velocity * self.direction[0]
        self.rect.y += self.velocity * self.direction[1]
