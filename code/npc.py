import pygame
from settings import *
from entity import Entity

class NPC(Entity):
    def __init__(self,pos,groups,ostacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Npc/tile000.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,HITBOX_OFFSET['player'])
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        self.hello_surface = self.font.render('Chao   con,   ta   la   Truong   Lang, Ta   o   day   de   giao   nhiem   vu   cho   con',False,'Black')
        self.hello_rect = self.hello_surface.get_rect(topleft = (50,600))
        self.talk_surface =self.font.render('Con   co   muon   nhan   nhiem vu   khong',False,'Black')
        self.talk_rect = self.talk_surface.get_rect(topleft = (50,600))
        self.conversation_surface = pygame.image.load('graphics/Dialog/DialogBox.png')
        self.conversation_rect = self.conversation_surface.get_rect(topleft =(0,480))