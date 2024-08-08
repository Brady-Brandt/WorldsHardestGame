import pygame
import os
from level import LEVELS, MAX_LEVEL
from menu import MainMenu, PauseMenu
from button import Button
from timer import * 


def pause_cb(btn, game):
    if game.pause_menu is None and game.main_menu is None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        game.pause_menu = PauseMenu(game.screen)
        game.timer.pause()

def pause_enter_cb(btn, game):
    if game.pause_menu is None and game.main_menu is None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        return True

def pause_leave_cb(btn, game):
    if game.pause_menu is None and game.main_menu is None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return False
       
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

        self.black = (0,0,0)
        pygame.font.init()

        self.timer = Timer(screen)

        self.gameFont = pygame.font.SysFont("Arial", 40)

        # play the background music
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'assets', 'background-music.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)


        self.save_file_path = os.path.join(script_dir, 'save.txt')
 
        self.main_menu = MainMenu(screen)
        self.pause_menu = None
        self.pause_btn = Button(screen,0,self.height-50,
                                "Pause",
                                self.gameFont,
                                fg=(255,255,255),
                                click=pause_cb,
                                m_enter=pause_enter_cb,
                                m_leave=pause_leave_cb)
 
    # draws the black bars with the level and the death count on the top and bottom of the screen
    def draw_hud(self):
        # draws black rectangle at top of screen
        pygame.draw.rect(self.screen, self.black, (0,0,self.width, 50))
        # draws black rectangle at bottom of screen
        pygame.draw.rect(self.screen, self.black, (0,self.height-50,self.width,50))

        self.timer.draw()

        # draws the level text
        level_text = self.gameFont.render("LEVEL: " + str(self.level),False, (255,255,255))		
        self.screen.blit(level_text, (5,0))

        # draws the fails text
        self.deaths = self.player.get_deaths()
        fail_text = self.gameFont.render("FAILS: " + str(self.deaths), False, (255,255,255))
        self.screen.blit(fail_text, (self.width - 200, 0))


    def save(self):
        output = f"{self.level},{self.deaths},{self.timer.ms}"
        with open(self.save_file_path, "w") as f:
            f.write("This is a save file DO NOT EDIT\n")
            f.write(output)



    def load_level(self):
        try:
            with open(self.save_file_path, "r") as f:
                lines = f.readlines()
                if len(lines) < 2:
                    return
                line = lines[1].split(',')
                if len(line) != 3:
                    return
                level = int(line[0])
                deaths = int(line[1])
                ms = int(line[2])

                if deaths < 0 or ms < 0:
                    return

                self.level = level
                self.deaths = deaths
                self.player.deaths = deaths
                self.timer.ms = ms
        except Exception:
            return

    def new_game(self):
        self.level = 1
        self.deaths = 0
        self.player.deaths = 0
        self.timer.ms = 0


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
                self.main_menu = MainMenu(self.screen)
                self.level = 1
                self.deaths = 0
                return

        # check if the level has been beaten to start a new one
        if self.current_level.completed:
            self.level += 1
            self.save()
            self.newLevel = True

    def draw_coin_count(self):
        total_coins = self.current_level.total_coins
        current_coins = self.current_level.coin_count

        # don't draw count if there are no coins in the level
        if total_coins == 0:
            return

        coin_count_text = self.gameFont.render(f"COINS: {current_coins} / {total_coins}", False, (255,255,255))
        self.screen.blit(coin_count_text, (275, 0))

  
    def play_game(self, dt):
        if self.main_menu is not None:
            self.main_menu.draw()
            return

        self.timer.update()
        self.draw_hud()
        self.pause_btn.draw()

        if self.pause_menu is not None:
            self.pause_menu.draw()
            dt = 0 # dt = 0 to create an illusion that the game is paused 

        self.start_level()
        self.current_level.draw_level(self.player, dt)
        self.player.move(dt, self.current_level.get_borders())
        if self.player.collide_enemy(self.current_level.get_enemies()):
            self.current_level.reset_coins()
        self.draw_coin_count()
