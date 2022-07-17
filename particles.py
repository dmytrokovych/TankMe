import pygame
from pygame import Vector2
from settings import *
from random import randrange


def make_particles(number, pos, groups):
    for i in range(number):
        Particle(pos, groups)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.timer = 10
        self.pos = Vector2(pos[0], pos[1])
        self.velocity = Vector2(
            randrange(-10, 10, 1) / 10, randrange(-10, 10, 1) / 10)

        self.make_image(10, self.pos)

    def make_image(self, size, pos):
        self.image = pygame.Surface([size, size])
        self.image.fill((255, int(size / 10 * 255), 0))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.pos += self.velocity
        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])
        self.timer -= 0.15

        if self.timer <= 0:
            self.kill()
        else:
            self.make_image(int(self.timer), self.rect.center)
