import pygame 
from button import Button

def start_game_cb(btn, game):
    game.main_menu.delete_buttons()
    game.main_menu = None
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

class MainMenu:
    def __init__(self, screen) -> None: 
        self.title = pygame.image.load("assets/game-title.png")
        self.screen = screen
        btn_color = (100, 149, 237)
        self.start_button = Button(self.screen, (125,500,200,75), btn_color, click=start_game_cb)
        self.load_button = Button(self.screen, (350,500,200,75), btn_color)
        self.select_button = Button(self.screen, (575,500,200,75), btn_color)


        self.title_font = pygame.font.SysFont("Arial", 35)
        self.black_title = pygame.font.SysFont("Arial", 30, bold=True)
        self.opt_font = pygame.font.SysFont("Palatino", 45,bold=True)

    def draw(self):
        black = (0,0,0)
        scr_w = self.screen.get_width()
        scr_h = self.screen.get_height()

        # black bar at top of screen
        pygame.draw.rect(self.screen, black, (0,0,scr_w, 50))
        # black bar at bottom of screen
        pygame.draw.rect(self.screen, black, (0,scr_h-50,scr_w,50))
      
        creator_text = self.title_font.render("CREATOR: Brady",False, (255,255,255))
        music_text = self.title_font.render("MUSIC: Techno", False, (255,255,255))
        self.screen.blit(creator_text, (5,0))
        self.screen.blit(music_text, (scr_w-250, 0))

        #draws python text python3
        python_text = self.black_title.render("Python 3", False, black)
        self.screen.blit(self.title, (100,50)) 
        self.screen.blit(python_text, (500, 125))

        # options
        play = self.opt_font.render("PLAY", False, (255,0,0))
        game = self.opt_font.render("GAME", False, (255,0,0))
        self.start_button.draw()
        self.screen.blit(play, (135, 500))
        self.screen.blit(game, (125, 545))


        load = self.opt_font.render("LOAD", False, (0,0,255))
        l_game = self.opt_font.render("GAME", False, (0,0,255))
        self.load_button.draw()
        self.screen.blit(load, (360, 500))
        self.screen.blit(l_game, (350,545))

        level = self.opt_font.render("LEVEL", False, (0,255,0))
        select = self.opt_font.render("SELECT", False, (0,255,0))
        self.select_button.draw()
        self.screen.blit(level, (575, 500))
        self.screen.blit(select, (575, 545))

    def delete_buttons(self):
        Button.delete_button(self.start_button)
        Button.delete_button(self.load_button)
        Button.delete_button(self.select_button)
