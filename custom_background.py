import pygame
import sys

from map_utility import Map


class Custom_background(Map):
    pygame.init()


    def __init__(self):
        super().__init__()
        self.running_game = True
        self.load_background(self.main_map)
        self.start()


    # place/remove a tile by clicking mouse
    #keep pressing the numbers and place tiles with left click
    #delete a tile with right click
    def place_tile(self):
        left_click, middle_click, right_click = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        x = int(x / 20)  # divide the x-pos by 10 because each tile is 10 pixel, so we have the exact coordinate of the
        # target tile
        y = int(y / 20)
        key = pygame.key.get_pressed()
        if key[pygame.K_1]:
            tile = 1
        elif key[pygame.K_2]:
            tile = 2
        elif key[pygame.K_0]:
            tile = 0
        else:
            tile = 0
        if left_click:
            self.background[y][x] = tile  # fill the background with the target-tile
        if right_click:
            tile = 0
            self.background[y][x] = tile
        if middle_click:
            self.reset_map(self.main_map)

    def start(self):

        while self.running_game:
            self.close_event()
            self.place_tile()
            self.render_background(self.screen)
            self.save_background_csv(self.main_map)
            self.update_screen()
