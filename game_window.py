import csv

import pygame
import sys

from map_utility import Map

from movement_utility import rot_center

from robot import PlayerRobot
from upload_effects import player_robot_img, player_gun_img, explosion_effect
from weather import Rain, Snow


class Game_window(Map):
    image_robot_player = player_robot_img
    image_gun_player = player_gun_img

    file = 'maps/background.csv'
    pygame.init()

    def __init__(self, weather):
        super().__init__()
        self.load_background(self.main_map)
        self.weather = weather
        self.game()

    # the game loop
    def game(self):
        run = True
        player = PlayerRobot((200, 200), 2, 2, 0.02)  # create a player_robot
        counter = 0
        rain = [Rain() for i in range(300)]
        snow = [Snow() for i in range(300)]
        while run:
            counter %= 60
            counter += 1

            self.close_event()
            self.render_background(self.screen,counter)

            player.check_wall_collision(self.wall_mask())


            player.move_robot()

            player.draw(self.screen, counter)
            player.check_water_collision(self.water_mask()[0], self.water_mask()[1], self.screen)
            player.check_lava_collision(self.lava_mask(), self.screen, counter)

            if self.weather == "rain":
                for i in range(Rain.start_rain(len(rain))):
                    rain[i].show()
                    rain[i].update()
            if self.weather == "snow":
                for i in range(Snow.start_snow(len(snow))):
                    snow[i].show()
                    snow[i].update()


            self.update_screen()

        pygame.quit()
