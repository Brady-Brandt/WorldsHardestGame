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
		self.pWidth = 20

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
	def stop_player(self, borders, direction):
		p_rect = self.get_rect()
		
		for rect in borders:
			rect = rect.get_rect()
			if p_rect.colliderect(rect):
				if direction == "RIGHT":
					self.x = rect.left - self.pWidth	

				elif direction == "LEFT":
					self.x = rect.right

				elif direction == "UP":
					self.y = rect.bottom
				else:
					self.y = rect.top - self.pWidth
				
		

	def move(self, dt, borders):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.x -= self.speed * dt
			self.stop_player(borders, "LEFT")
		if keys[pygame.K_RIGHT]:
			self.x += self.speed * dt
			self.stop_player(borders, "RIGHT")
		if keys[pygame.K_UP]:
			self.y -= self.speed * dt
			self.stop_player(borders, "UP")
		if keys[pygame.K_DOWN]:
			self.y += self.speed * dt
			self.stop_player(borders, "DOWN")
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

	
