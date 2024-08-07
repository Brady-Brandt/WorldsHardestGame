import pygame
from level import LEVELS, MAX_LEVEL
from menu import MainMenu

class Game:
    def __init__(self, screen, dims, player):
        self.screen = screen 
        self.width = dims[0]
        self.height = dims[1]
        self.player = player
        self.level = 1
        self.deaths = 0
        self.current_level = LEVELS[0](screen)

        self.newLevel = True
        self.pauseGame = False

        self.black = (0,0,0)
        pygame.font.init()

        self.gameFont = pygame.font.SysFont("Arial", 40)

        # play the background music
        pygame.mixer.init()
        pygame.mixer.music.load("assets/background-music.mp3")
        pygame.mixer.music.play(-1)
 
        self.main_menu = MainMenu(screen)
 
    # draws the black bars with the level and the death count on the top and bottom of the screen
    def draw_hud(self):
        # draws black rectangle at top of screen
        pygame.draw.rect(self.screen, self.black, (0,0,self.width, 50))
        # draws black rectangle at bottom of screen
        pygame.draw.rect(self.screen, self.black, (0,self.height-50,self.width,50))

        # draws the level text
        level_text = self.gameFont.render("LEVEL: " + str(self.level),False, (255,255,255))		
        self.screen.blit(level_text, (5,0))

        # draws the fails text
        fail_text = self.gameFont.render("FAILS: " + str(self.deaths), False, (255,255,255))
        self.screen.blit(fail_text, (self.width - 200, 0))
 

    # draws everything for the current level
    def draw_screen(self, dt):
        # update the death count for the hud
        self.deaths = self.player.get_deaths()
        self.draw_hud()
        self.current_level.draw_level(self.player, dt)


    def start_level(self):
        # creation of new level
        # create and load the level
        # set the player spawnpoint to the first checkpoint
        # spawn in the player
        if self.newLevel:
            if self.level > 0 and self.level < MAX_LEVEL + 1:
                self.current_level = LEVELS[self.level - 1](screen=self.screen) 
                spawn = self.current_level.checkpoints[0].get_spawn_loc()
                self.player.set_spawn_point(spawn[0], spawn[1])
                self.player.spawn()
                self.newLevel = False
            else:
                self.homeScreen = True
                return 

        # check if the level has been beaten to start a new one
        if self.current_level.completed:
            self.level += 1
            self.newLevel = True

    def draw_coin_count(self):
        total_coins = self.current_level.total_coins
        current_coins = self.current_level.coin_count

        # don't draw count if there are no coins in the level
        if total_coins == 0:
            return

        coin_count_text = self.gameFont.render(f"COINS: {current_coins} / {total_coins}", False, (255,255,255))
        self.screen.blit(coin_count_text, (275, 0))

    def pause_game(self):
        while self.pauseGame:
            pass

    def play_game(self, dt):
        if self.main_menu is not None:
            self.main_menu.draw()
            return

        self.start_level()
        self.draw_screen(dt)
        self.player.move(dt, self.current_level.get_borders())
        if self.player.collide_enemy(self.current_level.get_enemies()):
            self.current_level.reset_coins()
        self.draw_coin_count()
