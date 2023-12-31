import pygame
from settings import *

#This is a class that will be used to draw and create objects (rocks, trees,...)

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.image = surface
        self.sprite_type = sprite_type
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10) #changing the shape of the rect by making y smaller by 10px from top and down| x stay the same
