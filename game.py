import pygame
import parser
from enemy import Enemy
from objects import Rectangle, Border, Checkpoint

class Game:
	def __init__(self, screen, dims, player):
		self.screen = screen 
		self.width = dims[0]
		self.height = dims[1]
		self.player = player
		self.level = 1
		self.deaths = 0
		self.newLevel = True
		self.currentLevel = ""


	def play_game(self, dt):
		if self.newLevel:
			self.currentLevel = Level(self.screen, self.level)
			self.currentLevel.load_level()
			spawn = self.currentLevel.checkpoints[0].get_spawn_loc()
			self.player.set_spawn_point(spawn[0], spawn[1])
			self.player.spawn()
			self.newLevel = False

		self.currentLevel.draw_level(self.player)
		self.player.move(dt)
		

class Level:
	def __init__(self, screen, level):
		self.screen = screen
		self.hasLoaded = False		
		self.attributes = ["CHECKPOINT", "ENEMY", "BORDER", "RECT"]
		#these lists hold all of the objects in the current level
		self.checkpoints = []
		self.enemies = []
		self.borders = []
		self.rectangles = []
		self.level = level

	def parse_data(self, attributes):	
		#create all our object and add them to level arrays
		for obj in attributes:
			if len(obj) < 1:
				continue
			if obj[0] == "CHECKPOINT":
				checkpoint = Checkpoint(self.screen, obj[1])
				self.checkpoints.append(checkpoint)
			elif obj[0] == "BORDER":
				border= Border(self.screen, obj[1])
				self.borders.append(border)
			elif obj[0] == "RECT":
				rect = Rectangle(self.screen, obj[1])
				self.rectangles.append(rect)
			elif obj[0] == "ENEMY":
				enemy = Enemy(self.screen, obj[1])
				self.enemies.append(enemy)
					 
					
	def load_level(self):
		f = open("levels/level" + str(self.level) + ".txt", "r")
		data = f.read()
		
		blocks = data.split("END\n\n")
		for block in blocks:
			attributes = parser.parse_block(block)
			self.parse_data(attributes)
		self.hasLoaded = True
		f.close()

	def draw_level(self, player):
		player_rect = player.get_rect()
		for checkpoint in self.checkpoints:
			checkpoint.draw()
			# sets the players spawn to the checkpoint
			if checkpoint.get_rect().colliderect(player_rect):
				spawn = checkpoint.get_spawn_loc()
				player.set_spawn_point(spawn[0], spawn[1])
	
		for rectangle in self.rectangles:
			rectangle.draw()
		for border in self.borders:
			border.draw()
			border_rect = border.get_rect()
			# stops player from going through walls
			player.stop_player(border_rect)
	
		for enemy in self.enemies:
			enemy.draw()
