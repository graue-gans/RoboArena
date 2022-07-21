import csv

import pygame
import sys


from map_utility import Map
from robot import PlayerRobot

image_robot_player = pygame.transform.scale(pygame.image.load("images/robot.png"),(40,60))
image_gun_player = pygame.transform.scale(pygame.image.load("images/Gun_01.png"),(40,50))



class Game_window(Map):

    file = 'maps/background.csv'
    pygame.init()

    def __init__(self):
        super().__init__()
        self.load_background(self.main_map)
        self.game()

    # the game loop
    def game(self):
        run = True
        player = PlayerRobot((300, 200), 2, 1, 0.02, image_robot_player, image_gun_player)  # create a player_robot

        while run:
            self.close_event()
            self.render_background(self.screen)

            if player.colision_check(self.lava_mask(),image_robot_player):
                player.lava_collision()
            if player.colision_check(self.wall_mask(),image_robot_player):
                player.wall_collision()
            player.move_robot()
            player.draw_robot(self.screen)
            self.update_screen()
        pygame.quit()
