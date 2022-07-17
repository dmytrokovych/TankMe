import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        """
        pos :		    position of a tile
        groups :	    a list of sprite groups a tile is a part of
        sprite_type :   -
        surface :       -
        """

        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface

        if sprite_type == 'object':
            self.rect = self.image.get_rect(
                topleft=(pos[0], pos[1] - TILESIZE))
            self.hitbox =  self.rect.inflate(0, -TILESIZE)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -10)
