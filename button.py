import pygame


class Button:
    def __init__(self, screen, location,color):
        self.screen = screen
        self.location = location
        self.color = color

        self.rect = pygame.Rect(location)
        self.hand = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)



    # returns boolean tuple
    # first value indicates if it is hover over a button
    # second value indicates if it has been clicked
    def is_clicked(self):
        x,y = pygame.mouse.get_pos()

        if x <= self.rect.right and x >= self.rect.left and y >= self.rect.top and y < self.rect.bottom:
            # change the cursor to the hand if the mouse is over the button
            pygame.mouse.set_cursor(self.hand)
            buttons = pygame.mouse.get_pressed()
            # check for right click
            if buttons[0]:
                return (True, True)
            return (True, False)

         
        return (False, False)
