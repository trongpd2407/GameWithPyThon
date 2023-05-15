import pygame
from settings import *
class Quest():
    def __init__(self):
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        self.display_surface = pygame.display.get_surface()
        self.quest = self.font.render('Kill the raccoon boss',False,'Black')
        self.quest_rect = self.quest.get_rect(topleft = (1000,100))
        self.complete_quest = self.font.render('Complete',False,'Green')
        self.complete_quest_rect = self.complete_quest.get_rect(topleft = (1000,100))