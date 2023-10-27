import pygame

class Level:
    def __init__(self):
        self.visible_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

    #update and draw the game
    def run(self):
        pass