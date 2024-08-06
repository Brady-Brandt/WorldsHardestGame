import pygame
from enemy import Enemy


class Player:
    def __init__(self, screen, screen_dim):
        self.screen = screen
        self.width = screen_dim[0]
        self.height = screen_dim[1]
        self.image = pygame.image.load("assets/box.png")
        self.x = 250
        self.y = 250
        self.speed = 100
        self.spawn_point = (0, 0)
        self.p_width = 20
        self.deaths = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.p_width, self.p_width)

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def get_deaths(self):
        return self.deaths

    # called by the game at the start of each level or once
    # a checkpoint is reached to set the current spawn point
    def set_spawn_point(self, x, y):
        self.spawn_point = (x, y)

    # spawn the player at the current spawn point after death or
    # after a level is cleared
    def spawn(self):
        self.x = self.spawn_point[0]
        self.y = self.spawn_point[1]
        self.screen.blit(self.image, self.spawn_point)

    # stops the player if it collides with border
    def stop_player(self, borders, direction):
        p_rect = self.get_rect()

        for rect in borders:
            rect = rect.get_rect()
            if p_rect.colliderect(rect):
                if direction == pygame.K_RIGHT:
                    self.x = rect.left - self.p_width
                elif direction == pygame.K_LEFT:
                    self.x = rect.right
                elif direction == pygame.K_UP:
                    self.y = rect.bottom
                else:
                    self.y = rect.top - self.p_width

    def check_collision(self, rect, circle_center):
        # Find the closest point on the rectangle to the circle center
        closest_x = max(rect.left, min(circle_center[0], rect.right))
        closest_y = max(rect.top, min(circle_center[1], rect.bottom))

        # Calculate the distance between the circle center and this closest
        # point
        distance_x = circle_center[0] - closest_x
        distance_y = circle_center[1] - closest_y

        # If the distance is less than the circle's radius, there is a
        # collision
        distance_squared = distance_x**2 + distance_y**2
        return distance_squared < (Enemy.radius**2)

    # checks if the player has collide with an enemy
    def collide_enemy(self, enemies):
        p_rect = self.get_rect()
        for enemy in enemies:
            e_center = enemy.get_center()
            if self.check_collision(p_rect, e_center):
                self.spawn()
                self.deaths += 1
                return True
        return False

    def move(self, dt, borders):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed * dt
            self.stop_player(borders, pygame.K_LEFT)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed * dt
            self.stop_player(borders, pygame.K_RIGHT)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed * dt
            self.stop_player(borders, pygame.K_UP)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed * dt
            self.stop_player(borders, pygame.K_DOWN)
        # keeps the player on the screen
        if self.x < 0:
            self.x = 0
        elif self.x > self.width - self.p_width:
            self.x = self.width - self.p_width
        elif self.y > self.height - self.p_width:
            self.y = self.height - self.p_width
        elif self.y < 0:
            self.y = 0
        self.screen.blit(self.image, (self.x, self.y))
