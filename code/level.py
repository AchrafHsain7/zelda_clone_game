from typing import Sequence, Union
import pygame
from pygame.sprite import Sprite
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particle import AnimationPlayer

class Level:
    def __init__(self):

        #get the display surface: The Screen
        self.display_surface = pygame.display.get_surface()

        #the sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #attack assets
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #create the map
        self.create_map()

        #create the ui
        self.ui = UI()

        #loading particle effects
        self.animation_player = AnimationPlayer()

    def create_map(self):

        layouts = {
            "boundary": import_csv_layout('../map/map_FloorBlocks.csv'),
            "grass": import_csv_layout('../map/map_Grass.csv'),
            "object": import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }

        graphics = {
            "grass": import_folder('../graphics/Grass'),
            "objects": import_folder('../graphics/Objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        #create an invisible boundary tile
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        #create a grass tile
                        if style == 'grass':
                           random_grass_img = choice(graphics['grass'])
                           Tile((x,y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'grass', random_grass_img)
                        #create an object tile
                        if style == 'object':
                            object_img = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'object', object_img)
                        
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                (x, y), 
                                [self.visible_sprites], 
                                self.obstacle_sprites, 
                                self.create_attack, 
                                self.destroy_attack, 
                                self.create_magic)
                            else:
                                if col == '390':  monster_name = 'bamboo'
                                elif col == '391':  monster_name = 'spirit'
                                elif col == '392':  monster_name = 'raccoon' 
                                else :  monster_name = 'squid'
                                
                                Enemy(monster_name, (x,y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player, self.trigger_death_particle)
     
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
    
    def create_magic(self, style, strength, cost):
        print(style)
        print(strength)
        print(cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particle(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        elif target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #create particles
            self.animation_player.create_particle(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particle(self, pos, particle_type):
        self.animation_player.create_particle(particle_type, pos, [self.visible_sprites])

    #update and draw the game
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        #debug(self.player.status)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        #getting half of the screen width and height to keep player in the middle of the screen always 
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        #getting the offset
        self.offset.x = player.rect.x - self.half_width
        self.offset.y = player.rect.y - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)


