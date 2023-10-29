import pygame
from settings import *
from support import import_folder


#This is a class that will be used to draw and create objects (rocks, trees,...)

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        #setup graphics
        self.import_player_assets()
        self.status = 'down'

        #movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0


        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = "../graphics/player/"
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
                            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
                            'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attck':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
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
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print("attack")

        #magic input
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('magic')

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

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        #horizental movement
        self.hitbox.x += self.direction.x * speed
        self.collision('horizental')
        #vertical movement
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        #making the rect always follow the center of the hitbox
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizental':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
    
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.move(self.speed)
        
    
