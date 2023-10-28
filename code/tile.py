import pygame
from settings import *

#This is a class that will be used to draw and create objects (rocks, trees,...)

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10) #changing the shape of the rect by making y smaller by 10px from top and down| x stay the same
