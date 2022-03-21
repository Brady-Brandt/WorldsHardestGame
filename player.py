import pygame


class Player:
	def __init__(self, screen, screen_dim):
		self.screen = screen
		self.width= screen_dim[0]
		self.height = screen_dim[1]
		self.color = (255,0,0)
		self.image = pygame.image.load("assets/box.png")
		self.x = 250
		self.y = 250
		self.speed = 100
		self.spawnPoint = (0,0)

	#called by the game at the begininng of each level or once
	#a checkpoint is reached to set the current spawn point
	def set_spawn_point(self, x,y):
		self.spawnPoint = (x,y)
		self.x = x
		self.y = y

	#spawn the player at the current spawn point after death or 
	#after a level is cleared
	def spawn(self):
		self.screen.blit(self.image, self.spawnPoint)

	
	def move(self, dt):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.x -= self.speed * dt
		if keys[pygame.K_RIGHT]:
			self.x += self.speed * dt
		if keys[pygame.K_UP]:
			self.y -= self.speed * dt
		if keys[pygame.K_DOWN]:
			self.y += self.speed * dt	

		#keeps the player on the screen
		if self.x < 0:
			self.x = 0
		elif self.x > self.width - 25:
			self.x = self.width - 25
		elif self.y > self.height - 25:
			self.y = self.height - 25;
		elif self.y < 0:
			self.y = 0
		self.screen.blit(self.image, (self.x, self.y))
