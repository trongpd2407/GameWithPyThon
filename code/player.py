import pygame
from settings import *
from support import import_folder
from entity import Entity
class Player(Entity) :
    def __init__(self, pos, groups,obstacle_sprites,create_attack,destroy_weapon,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/tile000.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])
        #player graphics
        self.import_player_assets()
        self.status = 'down'
        self.pos = None
        #cooldown attack init
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        #weapon
        self.weapon_index = 0
        self.create_attack = create_attack
        self.destroy_weapon = destroy_weapon
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.switch_duration_cooldown = 200
        self.switch_weapon_time = None

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time= None

        #stats
        self.stats = {'hp' : 100, 'mp': 100,'attack' :10, 'magic' : 4,'speed' :5}
        self.max_stats = {'hp' : 200, 'mp': 150,'attack' :20, 'magic' : 10,'speed' :7}
        self.upgrade_cost = {'hp' : 100, 'mp': 150,'attack' :300, 'magic' : 300,'speed' :500}
        self.hp = self.stats['hp']
        self.mp = self.stats['mp']
        self.exp = 1000
        self.speed = self.stats['speed']
        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invunerability_duration = 500
        #import sound
        self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

        self.obstacle_sprites = obstacle_sprites
    
    def import_player_assets(self):
        character_path = 'graphics/Player/'
        self.animations ={'up' : [],'down' : [],'right' : [],'left' : [],
            'right_idle' : [],'left_idle' : [],'up_idle' : [],'down_idle' : [],
            'right_attack' : [],'left_attack' : [],'up_attack' : [],'down_attack' : [] }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        

    def input(self) :
        if not self.attacking:
            keys = pygame.key.get_pressed()
            
            #movenent input
            if keys[pygame.K_w] :
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s] :
                self.direction.y = 1
                self.status = 'down'
            else : self.direction.y = 0
            
            if keys[pygame.K_a] :
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d] :
                self.direction.x = 1
                self.status = 'right'
            else : self.direction.x = 0

            # attack input
            
            if keys[pygame.K_j] :
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
            
                
            # magic input
            if keys[pygame.K_k] :
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength']+self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style,strength,cost)


            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.switch_weapon_time = pygame.time.get_ticks()
                self.weapon_index +=1
                if self.weapon_index >= len(list(weapon_data.keys())):
                    self.weapon_index =  0
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.switch_magic_time = pygame.time.get_ticks()
                self.magic_index +=1
                if self.magic_index >= len(list(magic_data.keys())):
                    self.magic_index =  0
                self.magic = list(magic_data.keys())[self.magic_index]
            

    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status+'_idle'
            
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else :
                    self.status = self.status +'_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def animate(self):
        animation = self.animations[self.status]
        #loop over frame_index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        #set image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        #flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['dame']
        return base_damage+ weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        magic_damage = magic_data[self.magic]['strength']
        return base_damage+ magic_damage   

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]
    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]
    def mp_recovery(self):
        if self.mp < self.stats['mp']:
            self.mp += 0.01 * self.stats['magic']
        else:
            self.mp = self.stats['mp']
# cooldown
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacking :
            if current_time - self.attack_time > self.attack_cooldown+weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_weapon()
        if not self.can_switch_weapon:
            if current_time - self.switch_weapon_time > self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.can_switch_magic:
            if current_time - self.switch_magic_time > self.switch_duration_cooldown:
                self.can_switch_magic = True
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invunerability_duration:
                self.vulnerable = True
    
    def update(self) :
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.mp_recovery()
        
        
    