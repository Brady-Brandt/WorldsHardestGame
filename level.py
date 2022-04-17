import pygame
import parser
from objects import Checkpoint, Rectangle,Border,Coin
from enemy import Enemy
from player import Player

class Level:
    def __init__(self, screen, level):
        self.screen = screen
        self.hasLoaded = False		
        self.attributes = ["CHECKPOINT", "ENEMY", "BORDER", "RECT", "COIN"]
        #these lists hold all of the objects in the current level
        self.checkpoints = []
        self.enemies = []
        self.borders = []
        self.rectangles = []
        self.coins = []
        self.level = level
        self.levelComplete = False

    def parse_data(self, attributes):	
        #create all our object and add them to level arrays
        for obj in attributes:
            if len(obj) < 1:
                continue
            if obj[0] == "CHECKPOINT":
                checkpoint = Checkpoint(self.screen, obj[1], obj[2])
                self.checkpoints.append(checkpoint)
            elif obj[0] == "BORDER":
                border= Border(self.screen, obj[1])
                self.borders.append(border)
            elif obj[0] == "RECT":
                rect = Rectangle(self.screen, obj[1])
                self.rectangles.append(rect)
            elif obj[0] == "ENEMY":
                enemy = Enemy(self.screen, obj[1], obj[2])
                self.enemies.append(enemy)
        
            elif obj[0] == "COIN":
                coin = Coin(self.screen, obj[1])
                self.coins.append(coin)

    def load_level(self):
        f = open("levels/level" + str(self.level) + ".txt", "r")
        data = f.read()

        blocks = data.split("END\n\n")
        for block in blocks:
            attributes = parser.parse_block(block)
            self.parse_data(attributes)
        self.hasLoaded = True
        f.close()

    def draw_level(self, player, dt):
        player_rect = player.get_rect()
        for rectangle in self.rectangles:
            rectangle.draw()
        for border in self.borders:
            border.draw()	
        for checkpoint in self.checkpoints:
            checkpoint.draw()
            # sets the players spawn to the checkpoint
            if checkpoint.get_rect().colliderect(player_rect):

                # remove any coins collected from the list
                for index, coin in enumerate(self.coins):
                    if coin.isCollected:
                       self.coins.remove(index) 

                # if it is the last checkpoint we want to end the level
                if checkpoint.last_checkpoint():
                   self.levelComplete = True 
                spawn = checkpoint.get_spawn_loc()
                player.set_spawn_point(spawn[0], spawn[1])


        for enemy in self.enemies:
            enemy.draw(dt)

        for coin in self.coins:
            coin.draw()
            coin.collect_player(player_rect)

    def get_borders(self):
        return self.borders

    def get_enemies(self):
        return self.enemies

    def reset_coins(self):
        for coin in self.coins:
            coin.isCollected = False
