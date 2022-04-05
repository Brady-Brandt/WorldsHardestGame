import pygame


class Player:
	def __init__(self, screen, screen_dim):
		self.screen = screen
		self.width= screen_dim[0]
		self.height = screen_dim[1]
		self.image = pygame.image.load("assets/box.png")
		self.x = 250 
		self.y = 250
		self.speed = 100
		self.spawnPoint = (0,0)
		self.pWidth = 25

	def get_rect(self):
		return pygame.Rect(self.x, self.y, self.pWidth, self.pWidth)
	
	def set_location(self, x, y):
		self.x = x
		self.y = y

	#called by the game at the begininng of each level or once
	#a checkpoint is reached to set the current spawn point
	def set_spawn_point(self, x,y):
		self.spawnPoint = (x,y)

	#spawn the player at the current spawn point after death or 
	#after a level is cleared
	def spawn(self):
		self.x = self.spawnPoint[0]
		self.y = self.spawnPoint[1]
		self.screen.blit(self.image, self.spawnPoint)


	
	# stops the player if it collides with border
	def stop_player(self, rect):
		p_rect = self.get_rect()
		# right border collision
		if p_rect.left < rect.right and p_rect.left > rect.left and p_rect.bottom <= rect.bottom and p_rect.top >= rect.top:
			 self.x = rect.right

		# left border collision
		elif p_rect.right > rect.left and p_rect.right < rect.right and p_rect.bottom <= rect.bottom and p_rect.top >= rect.top:
				self.x = rect.left - self.pWidth

		# top border collsion
		elif p_rect.top < rect.bottom and p_rect.top > rect.top and p_rect.right <= rect.right and p_rect.left >= rect.left:	
				self.y = rect.bottom
		
		#bottom border collision
		elif p_rect.bottom > rect.top and p_rect.bottom < rect.bottom and p_rect.right <= rect.right and p_rect.left >= rect.left:
				self.y = rect.top - self.pWidth

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
		elif self.x > self.width - self.pWidth:
			self.x = self.width - self.pWidth
		elif self.y > self.height - self.pWidth:
			self.y = self.height - self.pWidth;
		elif self.y < 0:
			self.y = 0
		self.screen.blit(self.image, (self.x, self.y))

	