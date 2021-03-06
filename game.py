import pygame
from button import Button
from level import Level

class Game:
    def __init__(self, screen, dims, player):
        self.screen = screen 
        self.width = dims[0]
        self.height = dims[1]
        self.player = player
        self.level = 1
        self.deaths = 0
        self.currentLevel = ""

        self.homeScreen = True
        self.newLevel = True
        self.pauseGame = False

        self.black = (0,0,0)
        pygame.font.init()

        self.title = pygame.image.load("assets/game-title.png")
        self.gameFont = pygame.font.SysFont("Arial", 40)
        self.titleFont = pygame.font.SysFont("Arial", 35)
        self.blackTitle = pygame.font.SysFont("Arial", 30, bold=True)
        self.optionFont = pygame.font.SysFont("Palatino", 45,bold=True)

        # play the background music
        pygame.mixer.init()
        pygame.mixer.music.load("assets/background-music.mp3")
        pygame.mixer.music.play(-1)


        # create the homescreen buttons
        #(100, 149, 237)
        self.start_button = Button(self.screen, (125,500,200,75), (100, 149, 237))
        self.load_button = Button(self.screen, (350,500,200,75), (100, 149, 237))
        self.select_button = Button(self.screen, (575, 500,200,75), (100, 149, 237))

    def draw_homescreen(self):
        # black bar at top of screen
        pygame.draw.rect(self.screen, self.black, (0,0,self.width, 50))
        # black bar at bottom of screen
        pygame.draw.rect(self.screen, self.black, (0,self.height-50,self.width,50))

        
        creator_text = self.titleFont.render("CREATOR: BRADY BRANDT",False, (255,255,255))
        music_text = self.titleFont.render("MUSIC: Techno", False, (255,255,255))
        self.screen.blit(creator_text, (5,0))
        self.screen.blit(music_text, (self.width-250, 0))


        #draws python text python3
        python_text = self.blackTitle.render("Python 3", False, self.black)
        self.screen.blit(self.title, (100,50)) 
        self.screen.blit(python_text, (500, 125))

        # options
        play = self.optionFont.render("PLAY", False, (255,0,0))
        game = self.optionFont.render("GAME", False, (255,0,0))
        self.start_button.draw()
        self.screen.blit(play, (135, 500))
        self.screen.blit(game, (125, 545))


        load = self.optionFont.render("LOAD", False, (0,0,255))
        l_game = self.optionFont.render("GAME", False, (0,0,255))
        self.load_button.draw()
        self.screen.blit(load, (360, 500))
        self.screen.blit(l_game, (350,545))

        level = self.optionFont.render("LEVEL", False, (0,255,0))
        select = self.optionFont.render("SELECT", False, (0,255,0))
        self.select_button.draw()
        self.screen.blit(level, (575, 500))
        self.screen.blit(select, (575, 545))
        
                 
        select_hovering, select_clicked = self.select_button.is_clicked()
        load_hovering, load_clicked = self.load_button.is_clicked()
        start_hovering, start_clicked = self.start_button.is_clicked()
            

        # sets the cursor back to default if the mouse is not hovering
        # over and of the buttons
        if not select_hovering and not load_hovering and not start_hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 


        # start the game
        if start_clicked:
            self.homeScreen = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 

        # loads up a previous game
        # the level from the previous game is stored in the file below
        if load_clicked:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 
            with open("saved/level.txt") as f:
                self.level = int(f.readline())
                self.homeScreen = False
                return
            

    # draws the black bars with the level and the death count on the top and bottom of the screen
    # I know hud isn't the proper term but I didn't know what else to call it
    def draw_hud(self, dt):
        # draws black rectangle at top of screen
         pygame.draw.rect(self.screen, self.black, (0,0,self.width, 50))
         # draws black rectangel at bottom of screen
         pygame.draw.rect(self.screen, self.black, (0,self.height-50,self.width,50))

         # draws the level text
         level_text = self.gameFont.render("LEVEL: " + str(self.level),False, (255,255,255))		
         self.screen.blit(level_text, (5,0))

         # draws the fails text
         fail_text = self.gameFont.render("FAILS: " + str(self.deaths), False, (255,255,255))
         self.screen.blit(fail_text, (self.width - 200, 0))

         #fps_text = self.gameFont.render("FPS: " + str(int(1/dt)), False, (255, 255, 255))
         #self.screen.blit(fps_text, (0, self.height - 50))

    # draws everything for the current level
    def draw_screen(self, dt):
        # update the death count for the hud
        self.deaths = self.player.get_deaths()
        self.draw_hud(dt)
        self.currentLevel.draw_level(self.player, dt)


    def start_level(self):
        # creation of new level
        # create and load the level
        # set the player spawnpoint to the first checkpoint
        # spawn in the player
        if self.newLevel:
            # store the level in saved data 
            with open("saved/level.txt", "w") as f:
                f.seek(0)
                f.write(str(self.level))
                f.truncate()

            self.currentLevel = Level(self.screen, self.level)
            self.currentLevel.load_level()
            spawn = self.currentLevel.checkpoints[0].get_spawn_loc()
            self.player.set_spawn_point(spawn[0], spawn[1])
            self.player.spawn()
            self.newLevel = False

        # check if the level has been beaten to start a new one
        if self.currentLevel.levelComplete:
            self.level += 1
            self.newLevel = True

    def draw_coin_count(self): 
        current, max_count = self.currentLevel.get_coin_count()
        # dont draw count if there are no coins in the level
        if max_count == 0:
            return
        coin_count_text = self.gameFont.render("COINS: " + str(current) + "/" + str(max_count), False, (255,255,255))
        self.screen.blit(coin_count_text, (275, 0))

    def pause_game(self): 
        while self.pauseGame:
            pass

    def play_game(self, dt):
        if self.homeScreen:
            self.draw_homescreen()
            return

        self.start_level()
        self.draw_screen(dt) 
        self.player.move(dt, self.currentLevel.get_borders())
        if self.player.collide_enemy(self.currentLevel.get_enemies()):
            self.currentLevel.reset_coins()
        self.draw_coin_count()

