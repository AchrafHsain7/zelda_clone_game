import pygame

class Level:
    def __init__(self):

        #get the display surface: The Screen
        self.display_surface = pygame.display.get_surface()

        #the sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

    #update and draw the game
    def run(self):
        pass