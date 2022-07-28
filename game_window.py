import csv

import pygame
import sys


from map_utility import Map
from movement_utility import rot_center

from robot import EnemyRobot, PatrolRobot, PlayerRobot
from upload_effects import player_robot_img, player_gun_img, explosion_effect


image_robot = pygame.image.load("images/robot.png")
image_gun = pygame.image.load("images/Gun_01.png")


class Game_window(Map):
    image_robot_player = player_robot_img
    image_gun_player = player_gun_img


    file = 'maps/background.csv'
    pygame.init()

    def __init__(self):
        super().__init__()
        self.load_background(self.main_map)
        self.game()

    def init_enemy_robots(self):
        # init the enemy robots that are there from the start
        # e1 = EnemyRobot((810, 140), 180, image_robot, image_gun)
        return [] 

    def init_patrol_robots(self):
        p1 = PatrolRobot((810, 140), 2, 2, 0.02, image_robot, image_gun, (0, 1000), (0, 1000))
        return [p1]

    # the game loop
    def game(self):
        run = True

        player = PlayerRobot((100, 100), 2, 2, 0.02, self.image_robot_player, self.image_gun_player)  # create a player_robot
        counter = 0
        enemies = self.init_enemy_robots()
        patrols = self.init_patrol_robots()
        passed = False
        t = 0

        while run:
            counter %= 60
            self.close_event()
            self.render_background(self.screen)
            player.colision_check_lava(self.lava_mask())
            player.colision_check_wall(self.wall_mask(), counter)
            player.move_robot()

            # static enemy robots:
            for bot in enemies:
                if t > 3000:
                    bot.act(self.screen)
                    passed = True
                bot.move_robot()
                bot.draw(self.screen, counter)
                bot.update_projectiles(self.screen)
            if passed:
                t = 0
                passed = False
            # patrol robots:
            for bot in patrols:
                bot.move_robot()
                bot.draw(self.screen, counter)
                bot.update_projectiles(self.screen)

            player.draw(self.screen,counter)
            counter += 1

            dt = self.update_screen()
            t += dt
            

        pygame.quit()
