import pygame
import sys


class Main_menu():
    width = 1000
    height = 1000

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((Main_menu.width, Main_menu.height))
