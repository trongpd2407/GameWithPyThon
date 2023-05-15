import pygame
from settings import *
from random import choice, randint
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout,import_folder
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from npc import NPC
from mission import Quest

class Level:
    def __init__(self):
        #get display surface
        self.game_active = True
        self.keys = pygame.key.get_pressed()
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        #sprite group setup_ thiết lập nhóm các đối tượng
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        #attack sprite
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        #sprite setup
        self.create_map()
        #user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.quest = Quest()
        self.quest_accepted = False
        self.complete = False
        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self) :
        layouts = {
            'grass' : import_csv_layout('map/map1_Grass_1.csv'),
            'tree_rock' :import_csv_layout('map/map1_Tree_Rock_1.csv'),
            'boundary' : import_csv_layout('map/map1_FloorBlock_1.csv'),
            'house' :import_csv_layout('map/map1_House_1.csv'),
            'entity': import_csv_layout('map/map1_Entity_1.csv')
        }
        graphics = {
            'house' :import_folder('graphics/House'),
            'tree_rock' :import_folder('graphics/Tree_Rock')
        }
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row) :
                    if col != '-1':
                        x = col_index*TILESIZE
                        y = row_index*TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites],'invisible')
                        if style == 'grass':
                            grass_image = graphics['tree_rock'][int(col)]
                            Tile((x,y), [self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'grass',grass_image)
                        if style == 'tree_rock':
                            tree_rock_image = graphics['tree_rock'][int(col)]
                            Tile((x,y), [self.visible_sprites,self.obstacle_sprites],'tree_rock',tree_rock_image)
                        if style == 'house':
                            house_image = graphics['house'][int(col)]
                            Tile((x,y), [self.visible_sprites,self.obstacle_sprites],'house',house_image)
                        if style == 'entity':
                                
                            if col == '394' or col == '600':
                                if col == '394':
                                    self.player = Player((x,y),[self.visible_sprites],
                                                self.obstacle_sprites,self.create_attack,
                                                self.destroy_weapon,self.create_magic)
                                else : self.npc = NPC((x,y),[self.visible_sprites,self.obstacle_sprites],self.obstacle_sprites)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                elif col == '393': monster_name = 'squid'
                                self.enemy = Enemy(monster_name,(x,y),[self.visible_sprites,self.attackable_sprites],
                                self.obstacle_sprites,self.damage_player,
                                self.trigger_death_paticles,self.add_exp)
        
    
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
    
    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])
    
    def destroy_weapon(self):
        if self.current_attack :
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                for target_sprite in collision_sprites:
                    if target_sprite.sprite_type == 'grass':
                        pos = target_sprite.rect.center
                        for leaf in range(randint(3,6)):
                            self.animation_player.create_grass_particles(pos,[self.visible_sprites])
                        target_sprite.kill()
                    else:
                        target_sprite.get_damage(self.player,attack_sprite.sprite_type)
    
    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.hp -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_paticles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
        
    def add_exp(self,amount):
        self.player.exp += amount
    
    def toggle_menu(self):
        self.game_paused = not self.game_paused
    def quest_implement(self,player,npc,quest,enemy):
        if player.rect.colliderect(npc.rect) :
            npc.display_surface.blit(npc.conversation_surface,npc.conversation_rect)
            npc.display_surface.blit(npc.hello_surface,npc.hello_rect)
            self.quest_accepted = True
        if self.quest_accepted:
            
            if self.complete == True:
                quest.display_surface.blit(quest.complete_quest,quest.complete_quest_rect)
            else:
                quest.display_surface.blit(quest.quest,quest.quest_rect)
                if enemy.monster_name == 'raccoon':
                    print(enemy.monster_name)
            
            
    def check_game_over(self,player):
        if player.hp <=0:
            self.game_active = False
    def run(self):
        self.check_game_over(self.player)
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        self.quest_implement(self.player,self.npc,self.quest,self.enemy)
        if self.game_paused == True:
            self.upgrade.display()
        else:
            #update and draw the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_udate(self.player)
            self.player_attack_logic()
            
            
#lớp camera// overlap
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #general set up
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_heigth = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surface = pygame.image.load('Tiled/map1.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))



    def custom_draw(self,player):
        #getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_heigth
        #drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface,floor_offset_pos)

        #drawing spites
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    
    def enemy_udate(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)


