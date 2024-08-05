import pygame

class Enemy:
    color = (0,0,255)
    radius = 10
    # takes in starting location and list of 3d tuples
    # tuple specifies the x direction to move and the y
    # last one defines how far to move in that direction 
    def __init__(self, location, movement, speed=215, sync=True):
        self.x = location[0]
        self.y = location[1]
        self.speed = speed
        self.movement = movement      
        # index into movement array
        self.index = 0
        self.total_moved = 0 

        self.sync = sync
        self.startx = self.x
        self.starty = self.y

    def get_center(self):
        return (self.x, self.y)

    def get_radius(self):
        return Enemy.radius

    # returns the normalized sign of a value
    def get_dirrection(self,value):
        if value > 0:
            return 1
        elif value < 0:
            return -1
        return 0

    def update_movement(self):
        self.total_moved = 0
        self.index += 1
        if self.index == len(self.movement):
            if self.sync:
                self.x = self.startx
                self.y = self.starty
            self.index = 0

    # so we don't lose movement when the enemy switches direction 
    def overshoot(self, val): 
        self.update_movement()
        amount_to_move = self.movement[self.index][2]
        if amount_to_move == 0:
            self.update_movement()
            amount_to_move = self.movement[self.index][2]


        x = self.movement[self.index][0]
        y = self.movement[self.index][1]

        self.x += self.get_dirrection(x) * val
        self.y += self.get_dirrection(y) * val
        self.total_moved += val
        


    def draw(self, screen, dt):
        # the amount to move in one direction
        amount_to_move = self.movement[self.index][2]
        if amount_to_move == 0:
            self.update_movement()
            pygame.draw.circle(screen, Enemy.color, (self.x, self.y), Enemy.radius)
            return

        x = self.movement[self.index][0]
        y = self.movement[self.index][1]
        self.x += self.speed * self.get_dirrection(x) * dt
        self.y += self.speed * self.get_dirrection(y) * dt

        self.total_moved += self.speed * dt

        if self.total_moved >= amount_to_move:
            if x != 0 and y != 0:
                overshoot = self.total_moved - amount_to_move
                self.x -= overshoot * self.get_dirrection(x)
                self.y -= overshoot * self.get_dirrection(y)
                self.overshoot(overshoot)
            elif x != 0:
                overshoot = self.total_moved - amount_to_move
                self.x -= overshoot * self.get_dirrection(x)
                self.overshoot(overshoot)
            elif y != 0:
                overshoot = self.total_moved - amount_to_move
                self.y -= overshoot * self.get_dirrection(y)
                self.overshoot(overshoot)
            
            
        pygame.draw.circle(screen, Enemy.color, (self.x, self.y), Enemy.radius)
