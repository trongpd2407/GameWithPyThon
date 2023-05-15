import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    def __init__(self, monster_name,pos, groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        #graphic setup
        self.visible_sprite = groups
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        #respawn
        
        self.death_time = None
        self.respawn_time = 5000
        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        #stats
        self.monster_name = monster_name
        self.monster_info = monster_data[self.monster_name]
        self.health = self.monster_info['health']
        self.exp = self.monster_info['exp']
        self.speed = self.monster_info['speed']
        self.attack_damage = self.monster_info['damage']
        self.resistance = self.monster_info['resistance']
        self.attack_radius = self.monster_info['attack_radius']
        self.notice_radius = self.monster_info['notice_radius']
        self.attack_type = self.monster_info['attack_type']
        self.is_death = self.monster_info['is_death']
        self.position = pos
        
        #player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = self.monster_info['cooldown']
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        self.kill_time = None
        
        #invincibility timer
        self.vulnerable  = True
        self.hit_time = None
        self.invincibility_duration = 300
        #sound
        self.death_sound = pygame.mixer.Sound('audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(self.monster_info['attack_sound'])
        self.death_sound.set_volume(0.4)
        self.hit_sound.set_volume(0.4)
        self.attack_sound.set_volume(0.4)

    def import_graphics(self,name):
        self.animations = {'idle':[], 'move':[],'attack': [],'move_back':[]}
        main_path = f'graphics/Monster/{name}/'
        for animaton in self.animations.keys():
            if animaton == 'move_back':
                self.animations[animaton] = import_folder(main_path+'move')
            else :self.animations[animaton] = import_folder(main_path+animaton)
    
    def get_player_distance_and_direction(self,player):
        enermy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enermy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enermy_vec).normalize()
        else: 
            direction = pygame.math.Vector2()

        return (distance, direction)
    def get_started_distance_and_direction(self):
        enermy_vec = pygame.math.Vector2(self.rect.center)
        started_vec = pygame.math.Vector2(self.position)
        distance = (started_vec - enermy_vec).magnitude()
        if distance > 0:
            direction = (started_vec - enermy_vec).normalize()
        else: 
            direction = pygame.math.Vector2()

        return (distance, direction)
    
    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_and_direction(player)[1]
        elif self.status == 'move_back':
            self.direction = self.get_started_distance_and_direction()[1]
        else:
            self.directiona = pygame.math.Vector2()
    
    def get_status(self,player):
        distance = self.get_player_distance_and_direction(player)[0]
        distance2 = self.get_started_distance_and_direction()[0]
        if distance <= self.attack_radius and self.can_attack == True:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        elif distance2 > self.notice_radius:
            self.status = 'move_back'
        else:
            self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_and_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
    def check_death(self):
        if self.health <= 0 :
            self.death_time = pygame.time.get_ticks()
            self.is_death = 1
            self.remove(self.visible_sprite)
            self.trigger_death_particles(self.rect.center,self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()
        
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
