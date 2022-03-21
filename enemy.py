import pygame

class Enemy:
	def __init__(self, screen, x, y):
		self.screen = screen
		self.x = x
		self.y = y
		self.radius = 8
		self.color = (0,0,255)
		self.center = (self.x + self.radius, self.y + self.radius)
		self.switchx = False
		self.switchy = False
	
	def move(self, x, y):
		if self.switchx:
			self.x -= x
		else:
			self.x += x	
		
		if self.switchy:
			self.y -= y
		else:
			self.y += y
		
		if self.x > 500 - self.radius:
			self.switchx = True
		elif self.x < 0 + self.radius:
			self.switchx = False
		elif self.y < 0 + self.radius:
			self.switchy = False 
		elif self.y > 500 - self.radius:
			self.switchy = True 
	
		pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
	 	
		
