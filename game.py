import pygame
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
			self.newLevel = False

		self.currentLevel.draw_level()
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

	def parse_data(self, block):	
		#contains the variables in our level file
		variables = {}
		#removes the comments 
		lines = block.split("\n")
		attributes = []
		current_object = []
		for index, line in enumerate(lines):
			print(line)	
			# remove comments tabs and spaces
			line = line.split('#', 1)[0]
			line = line.replace('\t', "")
			line = line.replace(' ', "")
			
			#replace variabls with their assigned value
			for var in variables:
				line = line.replace(var[0], str(variables[var]))

			#check for assigment or declaration	
			if '=' in line: 
				declaration = line.split('=')
				#checks if the declartion is for attribute or variable
				if len(declaration[0]) < 2:
					variables[declaration[0]] = eval(declaration[1])
				else:
					#make the string tuples to int tuples
					if '(' in line:
						# remove the name of the attribute and the '='
						line = ''.join(declaration[1:])
						line = line.replace('(', "")
						line = line.replace(')', "")
						line = line.split(',')
						line = [eval(x) for x in line]
						#convert to int tuple to pass attributes
						current_object.append(tuple(line))	
					#just append attribute as int 	
					else:
						current_object.append(int(declaration[1]))	
			#add the attributes
			if line in self.attributes:
				current_object.append(line)
			#FIX THIS LINE
			if line == "SUB":
				attributes.append(current_object)
				current_object = []
		attributes.append(current_object)
		return attributes	

	def parse_attributes(self, attributes):
		#create all our object and add them to level arrays
		print(attributes)
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
					 
					
	def load_level(self):
		f = open("levels/level" + str(self.level) + ".txt", "r")
		data = f.read()
		
		blocks = data.split("END\n\n")
		for block in blocks:
			attributes = self.parse_data(block)
			self.parse_attributes(attributes)
		self.hasLoaded = True
		f.close()

	def draw_level(self):
		for checkpoint in self.checkpoints:
			checkpoint.draw()
		for rectangle in self.rectangles:
			rectangle.draw()
		for border in self.borders:
			border.draw()
