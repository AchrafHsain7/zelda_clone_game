import pygame
from settings import *

class UI:
    def __init__(self):
        #general 
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #stat bars
        self.health_bar = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        #wepaons graphics
        self.weapons_graphics = []
        for weapon in weapon_data.values():
            weapon_path = weapon['graphic']
            weapon_graphic = pygame.image.load(weapon_path).convert_alpha()
            self.weapons_graphics.append(weapon_graphic)

        self.magic_graphics = []
        for magic in magic_data.values():
            magic_path = magic['graphic']
            magic_graphic = pygame.image.load(magic_path).convert_alpha()
            self.magic_graphics.append(magic_graphic)

    def draw_bar(self, current_amount, max_amount, bg_rect, color):
        #draw the background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        #calculate new width of bar
        ratio = current_amount / max_amount
        current_width = ratio * bg_rect.width
        bar_rect = bg_rect.copy()
        bar_rect.width = current_width

        #draw the stat bar with border
        pygame.draw.rect(self.display_surface, color, bar_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def draw_exp(self, exp):
        text_surface = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surface.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        self.display_surface.blit(text_surface, text_rect)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surface = self.weapons_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(95, 630, has_switched)
        magic_surface = self.magic_graphics[magic_index]
        magic_rect = magic_surface.get_rect(center = bg_rect.center)
        self.display_surface.blit(magic_surface, magic_rect)

    def display(self, player):
        #draw stat bars
        self.draw_bar(player.health, player.stats['health'], self.health_bar, HEALTH_COLOR)
        self.draw_bar(player.energy, player.stats['energy'], self.energy_bar, ENERGY_COLOR)
        #draw player experience
        self.draw_exp(player.exp)
        #draw the weapon/magic selection
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)
