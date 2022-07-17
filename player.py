import pygame
from settings import *
from support import import_folder
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            'graphics/player_left/up/up_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics setup
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.5

        # movement
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 100
        self.attack_time = None
        self.key_set = {}

        self.obstacle_sprites = obstacle_sprites
        self.bullets = pygame.sprite.Group()

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']

    def import_player_assets(self, character_path):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def fire(self):
        self.bullets.add(
            Bullet((self.rect.centerx, self.rect.centery), self.direction, self.status))

    def input(self):
        keys = pygame.key.get_pressed()

        # movement input
        if keys[self.key_set['up']]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[self.key_set['down']]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[self.key_set['right']]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[self.key_set['left']]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if not self.attacking:
            # attack input
            if keys[self.key_set['fire']]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.fire()

    def get_bullets(self):
        return self.bullets

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def move(self, speed):
        """
        1. apply horizontal movement
        2. check horizontal collisions
        3. apply vertical movement
        4. check vertical collisions
        """
        if self.energy <= 0:
            speed = 0
            self.energy = 10

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

        if not 'idle' in self.status:
            self.energy -= 0.01
        

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                elif direction == 'vertical':
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def damage_collision(self, all_bullets):
        # collision with bullets
        if pygame.sprite.spritecollide(self, all_bullets, True):
            if self.health > 0:
                self.health -= 5
            else:
                self.health = 100

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)


class LeftPlayer(Player):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(pos, groups, obstacle_sprites)
        self.import_player_assets('graphics/player_left/')
        self.key_set = {'up': pygame.K_w,
                        'down': pygame.K_s,
                        'left': pygame.K_a,
                        'right': pygame.K_d,
                        'fire': pygame.K_SPACE}


class RightPlayer(Player):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(pos, groups, obstacle_sprites)
        self.import_player_assets('graphics/player_right/')
        self.key_set = {'up': pygame.K_UP,
                        'down': pygame.K_DOWN,
                        'left': pygame.K_LEFT,
                        'right': pygame.K_RIGHT,
                        'fire': pygame.K_RCTRL}
