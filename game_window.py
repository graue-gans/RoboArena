import csv

import pygame
import sys

from window import *
from robot import PlayerRobot


class Game_window(window):

    tile_set = {"0":(0,0,0), "1":(255,255,255), "2":(62,36,25)} #each tile can have different color
    file = 'maps/custom_background.csv'
    def __init__(self):
        pygame.init()
        #self.init_empty_background()

        self.load_background()
        self.game()


    def game(self):
        go = True
        player = PlayerRobot((200,200),4,2,0.02) #create a player_robot
        last_move = "stop"

        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            key = pygame.key.get_pressed()
            player.current_move = "neutral"

            if key[pygame.K_w]:
                player.current_move = "forwards"
                if player.change_direction_detection(last_move) and not (key[pygame.K_s]):
                    player.deceleration(last_move)
                else:
                    if not(key[pygame.K_s]):
                        last_move = player.current_move
                        player.move_robot(last_move)

            if key[pygame.K_s]:
                player.current_move = "backwards"
                if player.change_direction_detection(last_move) and not (key[pygame.K_w]):
                    player.deceleration(last_move)
                else:
                       if not (key[pygame.K_w]):
                            last_move = player.current_move
                            player.move_robot(last_move)
                       else:
                           player.deceleration(last_move)

            if key[pygame.K_d]:
                player.rotate_robot(right=True)

            if key[pygame.K_a]:
                player.rotate_robot(left=True)

            if key[pygame.K_r]:
                player.rotate_weapon(right=True)
            if key[pygame.K_q]:
                player.rotate_weapon(left=True)

            if player.current_move == "neutral":
                player.deceleration(last_move)




            self.render_background()
            self.tile_detection()

            player.draw_robot(self.screen,player.image,player.gun)
            pygame.display.update()

            self.clock.tick(60)





robo_arena = Game_window()