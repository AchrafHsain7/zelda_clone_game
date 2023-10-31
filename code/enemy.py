import pygame
from entity import Entity
from support import import_folder

class Enemy(Entity):
    def __init__(self,monster_name, pos, groups):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        #graphic setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

    def import_graphics(self, monster_name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/monsters/{monster_name}/'
        for animation in self.animations.keys():
            full_path =    main_path + animation 
            animation_surfaces = import_folder(full_path)
            self.animations[animation] = animation_surfaces
        
        