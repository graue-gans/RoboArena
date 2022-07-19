import csv

import pygame
import sys


from map_utility import Map
from robot import PlayerRobot

image_robot_player = pygame.image.load("images/robot.png")
image_gun_player = pygame.image.load("images/Gun_01.png")


class Game_window(Map):
    file = 'maps/background.csv'

    def __init__(self):

        self.load_background(self.file)
        self.game()

    # the game loop
    def game(self):
        go = True
        player = PlayerRobot((200, 200), 4, 1, 0.02, image_robot_player, image_gun_player)  # create a player_robot

        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.render_background()
            player.move_robot()
            player.draw_robot(self.screen)
            pygame.display.update()

            self.clock.tick(self.FPS)
