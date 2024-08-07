import pygame


def def_enter(btn, arg=None):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    return True

def def_leave(btn, arg=None):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    return False

def def_click(btn, arg=None):
    pass

class Button:
    buttons = []

    @staticmethod
    def add_button(button):
        Button.buttons.append(button)

    @staticmethod
    def delete_button(button):
        Button.buttons.remove(button)

    def __init__(self,screen,location,color, m_enter=def_enter, m_leave=def_leave, click=def_click):
        self.screen = screen
        self.location = location
        self.color = color
        self.rect = pygame.Rect(location)

        self.mouse_enter =  m_enter
        self.mouse_leave = m_leave
        self.click = click

        Button.add_button(self)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def handle_event(self, event, arg=None):
        if event.type == pygame.MOUSEMOTION:
            pos = event.__dict__["pos"]
            if self.rect.collidepoint(pos):
                return self.mouse_enter(self, arg)
            else:
                return self.mouse_leave(self,arg)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.__dict__["pos"]
            if self.rect.collidepoint(pos):
                return self.click(self,arg)
