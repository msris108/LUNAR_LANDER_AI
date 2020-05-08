'''
DESIGN OF THE NEURAL NETWORK:
	INPUT = ufo.x, base.mid
	OUTPUT = move_right() or move_left()
	activation funtion = tanh
'''


import pygame
import time
import os
import random
import pickle
import neat
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

		if self.y >= 500:
			self.y = 500
			return False

	def move_right(self):
		self.x = self.x + 2

		if self.x >= 740:
			self.x=740;

	def move_left(self):
		self.x = self.x -2

		if self.x <= 0:
			self.x=0;

	def move_down(self):
		self.y = 500

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



def draw_window(ufos, base, status, gen):
	score = 0

	win.blit(bg_img, (0, 0))
	win.blit(base_img, (0, 560))
	win.blit(base_img, (200, 560))
	win.blit(base_img, (400, 560))
	base.draw()

	text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
	win.blit(text, (WIN_WIDTH - 1- text.get_width(), 10))
    
	text = STAT_FONT.render("GEN: " + str(gen), 1, (255, 255, 255))
	win.blit(text, (10, 10))

	for ufo in ufos:
		ufo.draw()

	pygame.display.update()

def eval_genomes(genomes, config):
	global gen

	gen = 0
	gen += 1

	nets = [] # each genome(ge) are essentially neural nets
	ge = [] #to keep track of the returning birds
	ufos = []

	base = Base()

	for _, g in genomes:
		net = neat.nn.FeedForwardNetwork.create(g, config)
		nets.append(net)
		ufos.append(Ufo(365, 10))
		g.fitness = 0
		ge.append(g)

	clock = pygame.time.Clock()
	run = True
	status = False
	while run:
		clock.tick(20)
		#ufo.free_fall()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		if len(ufos) == 0:
			run = False
			break

		for x,ufo in enumerate(ufos):
			ufo.free_fall()
			output = nets[x].activate((ufo.x, base.mid,abs(base.mid - ufo.x) + abs(500 - ufo.y)))
			#output is a list of neurons but ours is only of one ref. OUTPUT
			if output[0] > 0.5:
				ufo.move_left()
				#ufo.move_down()
			else:
				ufo.move_right()
				#ufo.move_down()

		for x,ufo in enumerate(ufos):
			if ufo.y == 500 and ufo.x >= base.x and ufo.x <= base.x + base.GAP:
				status = True
				ge[x].fitness += 5
				ufos.pop(x)
				nets.pop(x)
				ge.pop(x)
			elif ufo.x >= base.x and ufo.x <= base.x + base.GAP:
				ge[x].fitness += 0.5
			elif ufo.y == 500:
				status = False
				ge[x].fitness -= 1
				ufos.pop(x)
				nets.pop(x)
				ge.pop(x)

		draw_window(ufos, base, status, gen)

def run(config_file):
	'''
	NEAT recomendation ref. documentation 
	'''

	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
	                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
	                     config_file)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	winner = p.run(eval_genomes, 50) #no of genrations to be run = 50
	'''
	To be sent the population values to the "main" which is the fitness function
	for 50 times 
	'''
	print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
	#ref run(config_path):
	local_dir  = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config-feedforward.txt")
	run(config_path)
