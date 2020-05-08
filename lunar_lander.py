import pygame
import time
import os
import random
import pickle

pygame.font.init()

STAT_FONT = pygame.font.SysFont("comicsans", 50)
WIN_WIDTH = 800
WIN_HEIGHT = 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Lunar Lander")

bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (800, 600))
rover_img = pygame.image.load(os.path.join("imgs","extraterrestrial.png"))
flag_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","flags.png")).convert_alpha())
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())


class Ufo:
	IMG = rover_img
	ANIMATION_TIME = 5

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMG

	def jump(self):
		self.vel = -0.5
		self.tick_count = 0
		self.height = self.y

	def free_fall(self):
		self.tick_count += 1
		d = self.vel*self.tick_count + 0.0005*(2)*self.tick_count**2

		if d >= 16:
			d = (d/abs(d)) * 16

		if d < 0:
			d -= 2

		self.y = self.y + d

		if self.y >= 400:
			self.y = 400
			return False

	def move_right(self):
		if self.y < 400:
			self.x = self.x + 17

			if self.x >= 740:
				self.x=740;

	def move_left(self):
		if self.y < 400:
			self.x = self.x -17

			if self.x <= 0:
				self.x=0;


	def draw(self):
		win.blit(self.IMG, (self.x, self.y))

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class Base:
	IMG = flag_img
	GAP = 140


	def __init__(self):
		self.y = 510
		self.x = random.randrange(0, 615)
		self.mid = self.x + (self.GAP*0.5)

	def draw(self):
		win.blit(flag_img, (self.x, self.y))
		win.blit(flag_img, (self.x + self.GAP, self.y))



def draw_window(ufo, base, status):
	score = 0
	gen = 0

	win.blit(bg_img, (0, 0))
	win.blit(base_img, (0, 560))
	win.blit(base_img, (200, 560))
	win.blit(base_img, (400, 560))
	base.draw()

	text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
	win.blit(text, (WIN_WIDTH - 1- text.get_width(), 10))
    
	text = STAT_FONT.render("GEN: " + str(gen), 1, (255, 255, 255))
	win.blit(text, (10, 10))

	ufo.draw()

	pygame.display.update()

def main():
	ufo = Ufo(365, 10)

	base = Base()

	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(30)
		ufo.free_fall()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			
			if event.type == pygame.KEYDOWN and ufo.y != 500:
				if event.key == pygame.K_LEFT:
					ufo.move_left()
				elif event.key == pygame.K_RIGHT:
					ufo.move_right()

		if ufo.y == 500 and ufo.x >= base.x and ufo.x <= base.x + base.GAP:
			status = True
		else:
			status = False

		draw_window(ufo, base, status)

main()
