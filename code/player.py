import pygame
from pygame.sprite import AbstractGroup
from settings import *

#This is a class that will be used to draw and create objects (rocks, trees,...)

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
