import pygame

class Enemy:
	def __init__(self, screen, location):
		self.screen = screen
		self.x = location[0]
		self.y = location[1]
		self.radius = 12
		self.color = (0,0,255)
		self.center = (self.x + self.radius, self.y + self.radius)
		self.speed = 5	

	def draw(self):
				
		pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
	 	
		
