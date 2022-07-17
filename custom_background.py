import pygame
import sys

from window import window


class custom_background(window):
    tile_set = {"0": (0, 0, 0), "1": (255, 255, 255), "2": (62, 36, 25)}  # each tile can have different color
    file = 'maps/custom_background.csv'
    def __init__(self):
        #self.init_empty_background()
        #self.save_current_background_csv()
        self.running_game = True
        self.load_background()
        self.start()



    def start(self):

        while self.running_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            self.tile_detection()
            self.render_background()
            self.save_current_background_csv()

            pygame.display.update()
            self.clock.tick(60)







c_b_1= custom_background()