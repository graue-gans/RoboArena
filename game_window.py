import csv

import pygame
import sys


from map_utility import Map
from movement_utility import rot_center

from robot import PlayerRobot
from upload_effects import player_robot_img, player_gun_img, explosion_effect


class Game_window(Map):
    image_robot_player = player_robot_img
    image_gun_player = player_gun_img


    file = 'maps/background.csv'
    pygame.init()

    def __init__(self):
        super().__init__()
        self.load_background(self.main_map)
        self.game()

    # the game loop
    def game(self):
        run = True
        player = PlayerRobot((100, 100), 2, 2, 0.02, self.image_robot_player, self.image_gun_player)  # create a player_robot
        counter = 0
        while run:
            counter %= 60
            self.close_event()
            self.render_background(self.screen)
            player.colision_check_lava(self.lava_mask())
            player.colision_check_wall(self.wall_mask(), counter)
            player.move_robot()
            player.draw(self.screen,counter)
            self.update_screen()

            counter += 1


        pygame.quit()
