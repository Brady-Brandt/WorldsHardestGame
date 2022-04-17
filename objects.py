import pygame

class Checkpoint:
    # takes in the location and boolean if it is the finish of the level
    def __init__(self, screen, location, is_end):
        self.screen = screen
        self.location = location
        self.color = (149,237,100)
        self.is_end = bool(is_end)

    def last_checkpoint(self):
        return self.is_end

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.location)


    def get_rect(self):
        return pygame.Rect(self.location)

    # returns the spawn location for the player in the middle of
    # the checkpoint
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

# coins they are going to be rects for us
class Coin:
    def __init__(self, screen, location):
        self.screen = screen
        self.location = (location[0], location[1], 8, 8)
        self.color = (155, 135, 12)

        # value if the coin has been collected
        self.isCollected = False
        # probably not best use of memory
        self.sound = pygame.mixer.Sound("assets/coin-sound.mp3")

    def draw(self):
        if self.isCollected:
            return
        x = self.location[0]
        y = self.location[1]
        w = self.location[2]
        #draw border around coin
        pygame.draw.line(self.screen, (0,0,0), (x,y), (x+w,y))
        pygame.draw.line(self.screen, (0,0,0), (x,y), (x,y+w))
        pygame.draw.line(self.screen, (0,0,0), (x+w,y), (x+w,y+w))
        pygame.draw.line(self.screen, (0,0,0), (x,y+w), (x+w,y+w))
        pygame.draw.rect(self.screen, self.color, self.location)


    def collect_player(self, player):
        if self.isCollected:
            return False

        if player.colliderect(pygame.Rect(self.location)):
            pygame.mixer.Sound.play(self.sound)
            self.isCollected = True
            return True
        return False
