import pygame
from settings import *
from support import import_folder
from entity import Entity


#This is a class that will be used to draw and create objects (rocks, trees,...)

class Player(Entity):

    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        #setup graphics
        self.import_player_assets()
        self.status = 'down'

        #movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.obstacle_sprites = obstacle_sprites

        #iframes
        self.vulnerable = False
        self.hurt_time = 0
        self.hurt_cooldown = 500

        #weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.switch_weapon_time = 0
        self.switch_weapon_cooldown = 200

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = 0
        self.switch_magic_cooldown = 200

        #stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.exp = 10
        self.speed = self.stats['speed']

    def import_player_assets(self):
        character_path = "../graphics/player/"
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
                            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
                            'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            #movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            #attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            #magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = self.magic
                strength = magic_data[self.magic]['strength'] + self.stats['magic']
                cost = magic_data[self.magic]['cost']
                self.create_magic(style, strength, cost)

            #switching weapons
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.switch_weapon_time = pygame.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= len(weapon_data):
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            #switching magic
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.switch_magic_time = pygame.time.get_ticks()
                self.magic_index += 1
                if self.magic_index >= len(magic_data):
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):

        #idle state animation
        if self.direction.x == 0 and self.direction.y == 0:
            if '_idle' not in self.status and not '_attack' in self.status:
                self.status = self.status + '_idle'
        #attack state animation
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if '_attack' not in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def get_full_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage 

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if current_time - self.switch_weapon_time >= self.switch_weapon_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.switch_magic_time >= self.switch_magic_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.hurt_cooldown:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        #seeting up the current animation image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flicker when hit
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        
        
    
