import pygame
from settings import *


class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        # for left player
        self.health_bar_rect_left = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect_left = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        # for right player
        self.health_bar_rect_right = pygame.Rect(WIDTH - HEALTH_BAR_WIDTH - 10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect_right = pygame.Rect(WIDTH - ENERGY_BAR_WIDTH - 10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color, position):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stats to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        if position == 'right':
            current_rect.left = bg_rect.left + (bg_rect.width - current_width)

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def display(self, player, position):
        if position == 'left':
            health_rect = self.health_bar_rect_left
            energy_rect = self.energy_bar_rect_left
        elif position == 'right':
            health_rect = self.health_bar_rect_right
            energy_rect = self.energy_bar_rect_right


        self.show_bar(player.health, player.stats['health'], health_rect, HEALTH_COLOR, position)
        self.show_bar(player.energy, player.stats['energy'], energy_rect, ENERGY_COLOR, position)
