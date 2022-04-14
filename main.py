import pygame
from player import Player
from enemy import Enemy
from game import Game

SCREEN_DIM = (800, 800)
WHITE = (255, 255, 255)
BACKGROUND = (135, 206, 235)
pygame.init()

screen = pygame.display.set_mode(SCREEN_DIM, vsync=1)
pygame.display.set_caption("World's Hardest Game")

player = Player(screen, SCREEN_DIM)
game = Game(screen, SCREEN_DIM, player) 
quit = False

last_frame = 0

while not quit:
	time = pygame.time.get_ticks()
	delta_time = (time - last_frame) / 1000.0
	last_frame = time

	screen.fill(BACKGROUND)	
	game.play_game(delta_time)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit = True

	pygame.display.flip()
