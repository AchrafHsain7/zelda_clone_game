from typing import Sequence, Union
import pygame
from pygame.sprite import Sprite
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):

        #get the display surface: The Screen
        self.display_surface = pygame.display.get_surface()

        #the sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #create the map
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    #update and draw the game
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        #getting half of the screen width and height to keep player in the middle of the screen always 
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        #getting the offset
        self.offset.x = -player.rect.x + self.half_width
        self.offset.y = -player.rect.y + self.half_height

        for sprite in self.sprites():
            offset_rect = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_rect)