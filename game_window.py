import csv

import pygame
import sys


from map_utility import Map
from robot import EnemyRobot, PlayerRobot

image_robot = pygame.image.load("images/robot.png")
image_gun = pygame.image.load("images/Gun_01.png")


class Game_window(Map):
    file = 'maps/background.csv'
    pygame.init()

    def __init__(self):
        super().__init__()
        self.load_background(self.file)
        self.game()

    def init_enemy_robots(self):
        # init the enemy robots that are there from the start
        e1 = EnemyRobot((110, 140), 180, image_robot, image_gun)
        return [e1] 

    def init_patrol_robots(self):
        return []

    # the game loop
    def game(self):
        run = True
        player = PlayerRobot((200, 200), 4, 2, 0.02, image_robot_player, image_gun_player)  # create a player_robot
        enemies = self.init_enemy_robots()
        patrols = self.init_patrol_robots()
        passed = False
        t = 0

        while run:
            self.close_event()
            self.render_background(self.screen)
            player.move_robot()
            player.draw_robot(self.screen)
            # static enemy robots:
            for bot in enemies:
                if t > 3000:
                    bot.act(self.screen)
                    passed = True
                bot.move_robot()
                bot.draw_robot(self.screen)
                bot.update_projectiles(self.screen)
            if passed:
                t = 0
                passed = False
            # patrol robots:
            for bot in patrols:
                bot.move_robot()
                bot.draw_robot(self.screen)
                bot.update_projectiles(self.screen)
            dt = self.update_screen()
            t += dt
        pygame.quit()
