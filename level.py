from chess import BLACK
import pygame
from settings import *
from tile import Tile
from player import LeftPlayer, RightPlayer
from debug import debug
from support import *
from random import choice
from ui import UI
from particles import Particle, make_particles


class Level:
    def __init__(self):

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map1/map_FloorBlocks.csv'),
            'grass':    import_csv_layout('map1/map_Grass.csv'),
            'object':   import_csv_layout('map1/map_Objects.csv'),
        }
        graphics = {
            'grass':    import_folder('graphics/Grass'),
            'objects':  import_folder('graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [
                                 self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        elif style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites], 'object', surf)

        self.player_left = LeftPlayer(
            (3*64, 3*64), [self.visible_sprites], self.obstacle_sprites)
        self.player_right = RightPlayer(
            (3*64, 4*64), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # update and draw the game

        self.bullets = self.player_left.get_bullets()
        self.bullets.add(self.player_right.get_bullets())
        self.visible_sprites.add(self.bullets)

        for bullet in self.bullets:
            if pygame.sprite.spritecollide(bullet, self.obstacle_sprites, False):
                make_particles(2, bullet.rect.center, [self.visible_sprites])
                bullet.kill()

        self.visible_sprites.custom_draw(self.player_left, pos='left')
        self.visible_sprites.custom_draw(self.player_right, pos='right')
        self.visible_sprites.update()

        self.player_left.damage_collision(self.bullets)
        self.player_right.damage_collision(self.bullets)

        self.ui.display(self.player_left, position='left')
        self.ui.display(self.player_right, position='right')


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # get the display surface (from anywhere)
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(
            'graphics/tilemap/ground1.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player, pos='left'):

        self.display_surface_half = pygame.Surface((WIDTH // 2, HEIGTH))
        self.display_surface_half.fill(WATER_COLOR)

        self.half_width = WIDTH // 4
        self.half_height = HEIGTH // 2

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface_half.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface_half.blit(sprite.image, offset_pos)

        if pos == 'left':
            self.display_surface.blit(self.display_surface_half, (0, 0))
        elif pos == 'right':
            self.display_surface.blit(
                self.display_surface_half, (WIDTH // 2, 0))

        pygame.draw.line(self.display_surface, BLACK,
                         (WIDTH // 2, 0), (WIDTH // 2, HEIGTH), 2)
