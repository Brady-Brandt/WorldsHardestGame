import pygame

class Dim: 
    def __init__(self, x,y,w,h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __iter__(self):
        l = (self.x, self.y, self.w, self.h)
        yield l

# actual background the player will be moving on
class Rectangle:
    color = (255, 255, 255)
    def __init__(self, dim):
        self.dim = dim
        self.left_border = Border.default()  
        self.right_border = Border.default() 
        self.top_border = Border.default()
        self.bottom_border =  Border.default()

    def add_borders(self, level):
        if self.left_border.is_valid():
            level.borders.append(self.left_border)
        if self.right_border.is_valid():
            level.borders.append(self.right_border) 
        if self.bottom_border.is_valid():
            level.borders.append(self.bottom_border) 
        if self.top_border.is_valid():
            level.borders.append(self.top_border)

    #returns the middle of the rectangle 
    # assumes the rectangle is a square 
    def calc_mid(self):
        x = self.dim.x
        y = self.dim.y
        w = self.dim.w
        h = self.dim.h
        result = ((w / 2) + x, (h / 2) + y)	
        return result            


    def draw(self, screen):
        pygame.draw.rect(screen, Rectangle.color, tuple(self.dim))


    def calc_borders(self, sides):
        border_width = 5 
        x = self.dim.x
        y = self.dim.y 
        w = self.dim.w 
        h = self.dim.h
        for side in sides:
            if side == 1:
                #left border 
                self.left_border = Border(Dim(x-border_width, y-border_width, border_width, h+border_width))
            elif side == 2:
                #top border
                self.top_border = Border(Dim(x-border_width, y-border_width, w+border_width,border_width))
            elif side == 3: 
                # right border 
                self.right_border = Border(Dim(w+x, y-border_width, border_width, h+border_width*2))
            elif side == 4:
                # bottom border 
                self.bottom_border = Border(Dim(x-border_width, y+h, w+border_width, border_width)) 


    # if a side doesn't draw borders 
    # there will be a gap in that side were the border should be 
    # this method is there to fix the gap if you need  
    # sides is a tuple of which side you want to fix 
    # 1 = left, 2 = top, 3 = right, 4 = bottom 
    def fix_dims(self, sides):
        bw = 5
        for side in sides:
            if side == 1:
                self.dim.x -= bw 
                self.dim.w += bw
            elif side == 2:
                self.dim.y -= bw
                self.dim.h += bw 
            elif side == 3:
                self.dim.w += bw 
            elif side == 4: 
                self.dim.h += bw


class Checkpoint(Rectangle):
    # takes in the location and boolean if it is the finish of the level
    color = (149,237,100)
    def __init__(self,dim,is_end, spawn_loc = None):
        super().__init__(dim)
        self.is_end = is_end
        self.spawn_loc = spawn_loc

    def last_checkpoint(self):
        return self.is_end

    def draw(self, screen):
        pygame.draw.rect(screen, Checkpoint.color, tuple(self.dim))

    def get_rect(self):
        return pygame.Rect((self.dim.x, self.dim.y, self.dim.w, self.dim.h))

    # returns the spawn location for the player in the middle of
    # the checkpoint
    def get_spawn_loc(self):
        if self.spawn_loc is None:
            x = self.dim.x
            y = self.dim.y
            w = self.dim.w 
            h = self.dim.h
            return (x + w / 2 - 20, y + h / 2 - 20)
        return self.spawn_loc



class Border:
    color = (0,0,0)
    width = 5
    @staticmethod
    def default():
        return Border(None)

    def is_valid(self):
        return self.dim is not None

    def __init__(self,dim):
        self.dim = dim

    def draw(self, screen):
        pygame.draw.rect(screen, Border.color, tuple(self.dim))

    def get_rect(self):
        return pygame.Rect((self.dim.x, self.dim.y, self.dim.w, self.dim.h))



# coins they are going to be rects for us
class Coin:
    color = (155, 135, 12)
    width = 8
    def __init__(self, location):
        self.location = (location[0], location[1], 8, 8)
        self.is_collected = False

        self.sound = pygame.mixer.Sound("assets/coin-sound.mp3")

    def draw(self, screen):
        if self.is_collected:
            return
        x = self.location[0]
        y = self.location[1]
        w = self.location[2]
        #draw border around coin
        pygame.draw.line(screen, (0,0,0), (x,y), (x+w,y))
        pygame.draw.line(screen, (0,0,0), (x,y), (x,y+w))
        pygame.draw.line(screen, (0,0,0), (x+w,y), (x+w,y+w))
        pygame.draw.line(screen, (0,0,0), (x,y+w), (x+w,y+w))
        pygame.draw.rect(screen, Coin.color, self.location)


    def collect_player(self, player):
        if self.is_collected:
            return False

        if player.colliderect(pygame.Rect(self.location)):
            pygame.mixer.Sound.play(self.sound)
            self.is_collected = True
            return True
        return False
