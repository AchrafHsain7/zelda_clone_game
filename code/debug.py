import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, x=20, y=20):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x,y))
    pygame.draw.rect(debug_surf, 'White', debug_rect)
    display_surface.blit(debug_surf, debug_rect)