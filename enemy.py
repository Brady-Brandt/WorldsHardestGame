import pygame

class Enemy:
    # takes in starting location and array of 3d tuples
    # tuple specifies the x direction to move and the y
    # final final indicates how many times to move in that direction
    def __init__(self, screen, location, movement):
        self.screen = screen
        
        self.x = location[0]
        self.y = location[1]
        self.radius = 10
        self.speed = 88
        self.color = (0,0,255)
        self.movement = movement
        
        # parse our movement tuple into an array of 3d vectors
        movement = []
        current = []
        for move in self.movement:
            current.append(move)
            if len(current) == 3:
                movement.append(current)
                current = []
        self.movement = movement


        # index into movement array
        self.index = 0

        self.startx = self.x
        self.starty = self.y

    def get_center(self):
        return (self.x, self.y)

    def get_radius(self):
        return self.radius

    # returns the normalized sign of a value
    def get_dirrection(self, value):
        if value < 0:
            return value / value * -1
        return value / value

    def draw(self, dt):

        # keeps track of how far to move in a direction
        diffx = abs(self.x - self.startx)
        diffy = abs(self.y - self.starty)

        # the amount to move in one direction
        amount_to_move = self.movement[self.index][2]

        if diffx >= amount_to_move:
            self.index += 1
            if self.index == len(self.movement):
                self.index = 0

            # make sure the bot doesn't end up to far of path if dt is too large
            dirrection = self.get_dirrection(self.movement[self.index][0])  
            self.x = self.startx + dirrection * amount_to_move * -1 
            self.startx = self.x

        if diffy >= amount_to_move:
            self.index += 1
            if self.index == len(self.movement):
                self.index = 0

            dirrection = self.get_dirrection(self.movement[self.index][1])
            self.y = self.starty + dirrection * amount_to_move * -1
            self.starty = self.y

        self.x += self.speed * self.movement[self.index][0] * dt
        self.y += self.speed * self.movement[self.index][1] * dt
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        
