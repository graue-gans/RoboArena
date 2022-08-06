import sys

import pygame


class Screen:
    pygame.init()
    width = 1000
    height = 1000
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    FPS = 60

    #close the window by pressing x
    def close_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    #update the window every 1/60 second
    def update_screen(self):
        pygame.display.update()
        return self.clock.tick(self.FPS)







