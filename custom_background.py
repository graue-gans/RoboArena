import pygame
import sys

from map_utility import Map


class Custom_background(Map):
    file = 'maps/custom_background.csv'

    def __init__(self):
        self.running_game = True
        self.load_background(self.file)
        self.start()

    # place/remove a tile by clicking mouse
    def place_tile(self):
        left_click, middle_click, right_click = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        x = int(x / 10)  # divide the x-pos by 10 because each tile is 10 pixel, so we have the exact coordinate of the
        # target tile
        y = int(y / 10)
        key = pygame.key.get_pressed()
        if key[pygame.K_1]:
            tile = 1
        elif key[pygame.K_2]:
            tile = 1
        elif key[pygame.K_3]:
            tile = 3
        else:
            tile = 0
        if left_click:
            self.background[x][y] = tile  # fill the background with the target-tile
        if right_click:
            tile = 0
            self.background[x][y] = tile
        if middle_click:
            self.reset_map(self.file)

    def start(self):

        while self.running_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.place_tile()
            self.render_background()
            self.save_background_csv(self.file)

            pygame.display.update()
            self.clock.tick(self.FPS)
