import pygame
import os
from button import Button

def start_game_cb(btn, game):
    game.main_menu.delete_buttons()
    game.main_menu = None
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    return True

class MainMenu:
    def __init__(self, screen) -> None:
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'assets', 'game-title.png')
        self.title = pygame.image.load(file_path)
        self.screen = screen       
        self.title_font = pygame.font.SysFont("Arial", 35)
        self.black_title = pygame.font.SysFont("Arial", 30, bold=True)
        self.opt_font = pygame.font.SysFont("Palatino", 45,bold=True)

        self.start_button = Button(self.screen, 125, 500, "PLAY\nGAME",self.opt_font,
                                   fg=(255,0,0),
                                   click=start_game_cb)

        self.load_button = Button(self.screen, 350,500,
                                  "LOAD\nGAME", 
                                  self.opt_font,
                                  fg=(0,0,255))

        self.select_button = Button(self.screen, 575,500, "LEVEL\nSELECT",
                                    self.opt_font,
                                    fg=(0,255,0))


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

        self.start_button.draw()
        self.load_button.draw()
        self.select_button.draw()


    def delete_buttons(self):
        Button.delete_button(self.start_button)
        Button.delete_button(self.load_button)
        Button.delete_button(self.select_button)



def main_menu_cb(btn, game):
    game.pause_menu = None
    game.main_menu = MainMenu(game.screen)
    return True

def resume_cb(btn, game):
    game.pause_menu = None
    return True


def pause_menu_enter(btn, game):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    btn.bg = (255, 244, 79)
    return True

def pause_menu_leave(btn, game):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    btn.bg = None
    return False


class PauseMenu:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 35)
        self.resume_btn = Button(self.screen, 300,50, "Resume Game",
                                 self.font,
                                 m_enter=pause_menu_enter,
                                 m_leave=pause_menu_leave,
                                 click=resume_cb)
        self.menu_btn = Button(self.screen, 320,100, "Main Menu",
                               self.font, 
                               m_enter=pause_menu_enter,
                               m_leave=pause_menu_leave,
                               click=main_menu_cb)
        # adds a dark tint to the screen
        self.faded_screen = pygame.Surface((screen.get_width(),
                                            screen.get_height()),
                                           pygame.SRCALPHA)
        self.faded_screen.fill((12, 46, 106, 110))

    def draw(self):
        self.screen.blit(self.faded_screen, (0,0))
        self.resume_btn.draw()
        self.menu_btn.draw()

    def __del__(self):
        Button.delete_button(self.resume_btn)
        Button.delete_button(self.menu_btn)
