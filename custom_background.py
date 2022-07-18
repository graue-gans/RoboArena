import pygame
import sys

from window import window


class custom_background(window):
    tile_set = {"0": (0, 0, 0), "1": (255, 255, 255), "2": (62, 36, 25), "3":(100,100,100)}  # each tile can have different color
    file = 'maps/custom_background.csv'
    def __init__(self):
        self.init_empty_background()
        self.running_game = True
        #self.save_current_background_csv()
        self.load_background()
        self.start()

    def place_tile(self):
        left_click, middle_click, right_click = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        x = int(x / 10)
        y = int(y / 10)
        key = pygame.key.get_pressed()
        if key[pygame.K_1]:
            color = 0
        elif key[pygame.K_2]:
            color = 1
        elif key[pygame.K_3]:
            color = 2
        elif key[pygame.K_4]:
            color = 3
        else:
            color = 0
        if left_click:
            self.background[x][y] = color
        if right_click:
            color = 0
            self.background[x][y] = color


    def start(self):

        while self.running_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            self.place_tile()
            self.render_background()
            self.save_current_background_csv()

            pygame.display.update()
            self.clock.tick(60)







