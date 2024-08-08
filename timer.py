import pygame 


class Timer:
    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.ms = 0
        self.save = 0
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 35)

    def update(self):
        self.ms += self.clock.tick()

    def start(self):
        self.unpause()
        self.ms = 0

    def pause(self):
        self.save = self.ms

    def unpause(self):
        self.clock.tick()
        self.ms = self.save
        self.save = 0

    def __str__(self):
        ms = self.ms
        # if save is non-zero that means we are paused
        if self.save != 0:
            ms = self.save
        seconds = ms // 1000 % 60
        minutes = (ms // 60000) % 60
        hours = minutes // (60000 * 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def draw(self):
        time = self.__str__()
        text = self.font.render(time, False, (0,0,0))
        self.screen.blit(text, (0, 50))
