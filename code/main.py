import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		self.display_sur = pygame.display.get_surface()
		self.game_intro = True
		pygame.display.set_caption('SamuraiAdventure')
		self.clock = pygame.time.Clock()
		self.level = Level()
		self.game_active = True
		self.font_over = pygame.font.Font(UI_FONT,50)
		self.text_intro =['WASD   de   di   chuyen','J   de   danh', 'K   de   dung   spell','Q   E   de   doi   vu   khi,  spell','M   de   su   dung   exp   tang   chi   so','An   phim   Space   de   bat   dau']
		self.name = pygame.image.load('graphics/name.png')
		self.name_rect = self.name.get_rect(center = (640,100))
		self.background = pygame.image.load('graphics/background.png')
		self.background_rect = self.name.get_rect(topleft = (0,0))
		self.intro_surface = None
		self.intro_rect = None
		self.finish_surface = self.font_over.render('GAME OVER',False,'Red')
		self.finish_rec = self.finish_surface.get_rect(center = (640,300))
		self.respawn_surface = self.font_over.render('press   space   to   respawn',False,'White')
		self.respawn_rec = self.respawn_surface.get_rect(center = (640,400))
	
	def intro(self):
		y = 200
		self.display_sur.blit(self.background,self.background_rect)
		self.display_sur.blit(self.name,self.name_rect)
		for i in self.text_intro:
			self.intro_surface = self.font_over.render(i,True,'Black')
			self.intro_rect = self.intro_surface.get_rect(topleft = (200,y))
			self.display_sur.blit(self.intro_surface,self.intro_rect)
			y += 50


	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if self.game_intro:
					if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_SPACE:
								self.game_intro = False
				else:	
					if self.level.game_active:
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_m:
								self.level.toggle_menu()
					else :
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_SPACE:
								self.level.game_active = True
								self.level.player.hp = 50
								self.level.player.mp = 50
								self.level.player.exp = 0
			if self.game_intro:
				self.intro()
			else:
				if self.level.game_active:
					self.screen.fill('black') 
					self.level.run()
				else:
					self.level.display_surface.fill('black')
					self.level.display_surface.blit(self.finish_surface,self.finish_rec)
					self.level.display_surface.blit(self.respawn_surface,self.respawn_rec)
			pygame.display.update()
			self.clock.tick(FPS)			

if __name__ == '__main__' :
	game = Game()
	game.run()