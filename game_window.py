import csv

import pygame
import sys

from window import *
from robot import PlayerRobot


class Game_window(window):

    tile_set = {"0":(0,0,0), "1":(255,255,255), "2":(62,36,25)} #each tile can have different color
    file = 'maps/background.csv'
    def __init__(self):
        pygame.init()
        self.init_empty_background()
        self.load_background()
        self.game()


    def game(self):
        go = True
        player = PlayerRobot((200,200),4,2,0.02) #create a player_robot

        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            key = pygame.key.get_pressed()
            moving = False




            if key[pygame.K_w] and key[pygame.K_s]:
                pass

            elif key[pygame.K_w]:
                moving = True
                player.last_moving_direction = 0
                if key[pygame.K_s]:
                    player.deceleration_forward()
                else:
                    player.move_forward()


            elif key[pygame.K_s]:
                moving = True
                player.last_moving_direction = 1
                if key[pygame.K_w]:
                    player.deceleration_backward()
                else:
                    player.move_backward()

            if key[pygame.K_d]:
                player.rotate_robot(right=True)

            if key[pygame.K_a]:
                player.rotate_robot(left=True)

            if key[pygame.K_r]:
                player.rotate_weapon(right=True)
            if key[pygame.K_q]:
                player.rotate_weapon(left=True)


            if not moving and player.last_moving_direction == 0:
                player.deceleration_forward()
            if not moving and player.last_moving_direction == 1:
                player.deceleration_backward()





            self.render_background()


            player.draw_robot(self.screen,player.image,player.gun)
            pygame.display.update()

            self.clock.tick(60)





