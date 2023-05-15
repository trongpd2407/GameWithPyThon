import pygame
from settings import *

class Upgrade:
    def __init__(self,player):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_name = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        self.max_value = list(player.max_stats.values())
        #item dimensions
        self.height = self.display_surface.get_size()[1]*0.8
        self.width = self.display_surface.get_size()[0] //6
        self.create_item()
       #selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_d] and self.selection_index< self.attribute_number-1:
                self.selection_index+=1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_a] and self.selection_index >= 1:
                self.selection_index-=1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_f]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)


    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True
    def create_item(self):
        self.item_list = []
        for item,index in enumerate(range(self.attribute_number)):
            #horizontal positon
            full_width =self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment- self.width) // 2
            #vertical position
            top = self.display_surface.get_size()[1]*0.1
            #create object
            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)
    def display(self):
        self.input()
        self.selection_cooldown()
        for index,item in enumerate(self.item_list):
            name = self.attribute_name[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_value[index]
            cost = self.player.get_cost_by_index(index)
            item.display(self.display_surface,self.selection_index,name,value,max_value,cost)

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
    
    def display_name(self,surface,name,cost,selected):
        color =TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        title_surface = self.font.render(name,False,color)
        title_rect = title_surface.get_rect(midtop = self.rect.midtop+ pygame.math.Vector2(0,20))
        title_surface2 = self.font.render(str(cost),False,color)
        title_rect2 = title_surface2.get_rect(midbottom = self.rect.midbottom+ pygame.math.Vector2(0,-20))
        
        surface.blit(title_surface,title_rect)
        surface.blit(title_surface2,title_rect2)

    def display_bar(self,surface,value,max_value,selected):
        #drawing setup
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        #bar setup
        full_heigth = bottom[1]- top[1]
        relative_number = (value / max_value)*full_heigth
        value_rect = pygame.Rect(top[0]-15,bottom[1]-relative_number,30,10)
        #draw elements
        pygame.draw.line(surface,color,top,bottom)
        pygame.draw.rect(surface,color,value_rect)
    
    def trigger(self,player):
        upgrade_attrribute = list(player.stats.keys())[self.index]
        if player.exp >= player.upgrade_cost[upgrade_attrribute] and player.stats[upgrade_attrribute] < player.max_stats[upgrade_attrribute]:
            player.exp -= player.upgrade_cost[upgrade_attrribute]
            player.stats[upgrade_attrribute] *= 1.2
            player.upgrade_cost[upgrade_attrribute]*= 1.4
        if player.stats[upgrade_attrribute] > player.max_stats[upgrade_attrribute]:
            player.stats[upgrade_attrribute] = player.max_stats[upgrade_attrribute]

    def display(self,surface, selection_number,name,value,max_value,cost):
        if self.index == selection_number:
            pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
        else:
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
        self.display_name(surface,name,cost,self.index == selection_number)
        self.display_bar(surface,value,max_value,self.index == selection_number)