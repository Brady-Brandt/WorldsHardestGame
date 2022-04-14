import pygame


class Checkpoint:
    # takes in the location and boolean if it is the finish of the level
    def __init__(self, screen, location, is_end):
        self.screen = screen
        self.location = location
        self.color = (0,255,0)#GREEN
        self.is_end = bool(is_end)

    def last_checkpoint(self):
        return self.is_end

    def draw(self):	
        pygame.draw.rect(self.screen, self.color, self.location)


    def get_rect(self):
        return pygame.Rect(self.location)

    def get_spawn_loc(self):
        x,y,w,h = self.location
        return (x + w / 2 - 20, y + h / 2 - 20)



class Border:
    def __init__(self, screen, location):
        self.screen = screen
        self.location = location
        self.color = (0,0,0) #black

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.location)

    def get_rect(self):
        return pygame.Rect(self.location)

# actual background the player will be moving on 
class Rectangle:
    def __init__(self, screen, location):
        self.screen = screen
        self.location = location 
        self.color = (255, 255, 255)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.location)
