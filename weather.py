from random import randint

import pygame

from screen import Screen


class Weather(Screen):

    def __init__(self):
        self.x = randint(0, self.width)
        self.y = randint(0, self.height)
        self.start_positionx = 0
        self.start_positiony = 0


class Rain(Weather):
    rain_number = 0
    #show the rain
    def show(self):
        pygame.draw.line(self.screen, (144, 153, 161), (self.x, self.y), (self.x, self.y + 2), 1)
    #update each rain
    def update(self):
        if self.y >= self.start_positiony + randint(100, 300):
            self.y = randint(0, self.width)
            self.x = randint(0, self.width)
            self.start_positionx = self.x
            self.start_positiony = self.y
        else:
            self.y = 2 + self.y * 1.04
            self.x += randint(0, 4)
    #make more rains at the beginning
    @staticmethod
    def start_rain(amount_of_rain):
        if Rain.rain_number + 1 < amount_of_rain:
            Rain.rain_number += 1
        return Rain.rain_number


class Snow(Weather):
    snow_number = 0

    def show(self):
        pygame.draw.line(self.screen, (250, 250, 250), (self.x, self.y), (self.x, self.y + randint(1, 5)), 1)

    def update(self):
        if self.y >= self.start_positiony + randint(100, 300):
            self.y = randint(0, self.width)
            self.x = randint(0, self.width)
            self.start_positionx = self.x
            self.start_positiony = self.y
        else:
            self.y = 1 + self.y * 1.005
            self.x += randint(-1,1) + randint(0,4) # snow has needs a small left and right movement and move right to
            #have a 3d look

    @staticmethod
    def start_snow(amount_of_rain):
        if Snow.snow_number + 1 < amount_of_rain:
            Snow.snow_number += 1
        return Snow.snow_number
