import csv

import pygame
import sys


from map_utility import Map
from robot import PlayerRobot

image_robot_player = pygame.image.load("images/robot.png")
image_gun_player = pygame.image.load("images/Gun_01.png")


class Game_window(Map):
    file = 'maps/background.csv'
    pygame.init()

    def __init__(self):
        super().__init__()
        self.load_background(self.file)
        self.game()

    # the game loop
    def game(self):
        run = True
        player = PlayerRobot((200, 200), 4, 2, 0.02, image_robot_player, image_gun_player)  # create a player_robot

        while run:
            self.close_event()
            self.render_background(self.screen)
            player.move_robot()
            player.draw_robot(self.screen)
            self.update_screen()
        pygame.quit()
