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

    def __init__(self,screen,x,y,
                 text,
                 font,
                 fg = (0,0,0),
                 bg = None,
                 m_enter=def_enter,
                 m_leave=def_leave, click=def_click):

        self.screen = screen
        self.fg = fg
        self.bg = bg
        self.text = text
        self.font = font

        total_width = 0
        total_height = 0

        self.surfaces = []

        for line in self.text.split('\n'):
            (w,h)= self.font.size(line)
            total_width = max(w, total_width)
            total_height += h
            self.surfaces.append(self.font.render(line, False, self.fg))


        self.rect = pygame.Rect((x,y,total_width, total_height))
        self.mouse_enter =  m_enter
        self.mouse_leave = m_leave
        self.click = click

        Button.add_button(self)

    def draw(self):
        prev_h = 0
        if self.bg is not None:
            pygame.draw.rect(self.screen, self.bg, self.rect)
        for surface in self.surfaces:
            self.screen.blit(surface, (self.rect.x, self.rect.y + prev_h))
            prev_h += surface.get_height()


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
