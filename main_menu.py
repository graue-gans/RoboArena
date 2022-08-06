import pygame
import sys

from Game_Info import font3
from custom_background import Custom_background
from game_window import Game_window
from screen import Screen


class Main_menu(Screen):
    pygame.font.init()
    font = pygame.font.SysFont('comic Sans MS', 20)

    def __init__(self):
        self.button_aktiv = False
        self.start_main_menu()


    # main_menu infinit loop
    def start_main_menu(self):
        run = True
        while run:
            self.close_event()
            self.click = pygame.mouse.get_pressed()
            self.screen.fill((0, 0, 0))  # fill the screen with black
            self.mouse = pygame.mouse.get_pos()
            self.robo_arena_logo(self.screen)
            # inputs:
            # position x , position y, button width, button_height, rgb-color-inactive,rgb-color active, text-on-button
            self.button(350, 500, 300, 80, (127, 125, 125), (255, 255, 255), "play")
            self.button(350, 600, 300, 80, (127, 125, 125), (255, 255, 255), "map")
            self.button(350, 700, 300, 80, (127, 125, 125), (255, 255, 255), "exit")
            self.update_screen()
        pygame.quit()

    # create a text with given font and the textarea
    def textObjekt(self, text, font,rgb):
        text_rect = font.render(text, True, rgb)
        return text_rect, text_rect.get_rect()

    # create the buttons with a text on it
    def button(self, x, y, width, height, color_in_active, color_active, massage):
        # if the mouse is over a  button:
        if x < self.mouse[0] < x + width and y < self.mouse[1] < y + height:
            # draw a button with a active_color
            pygame.draw.rect(self.screen, color_active, (x, y, width, height))
            # if the left mouse button is pressed and the button is inactive:
            if self.click[0] == 1 and self.button_aktiv == False:
                # actitve the button
                self.button_aktiv = True
                # start the game, if play-button is pressed
                if massage == "play":
                    self.chooseWeather()
                # create a map , if map-button is pressed
                elif massage == "map":
                    # go to the setting window, if the setting-button is pressed
                    c_b_1 = Custom_background()
                # and quit when exit-button is pressed
                elif massage == "exit":
                    sys.exit()
                elif massage == "rain":
                    # go to the setting window, if the setting-button is pressed
                    robo_arena = Game_window("rain")
                # and quit when exit-button is pressed
                elif massage == "snow":
                    robo_arena = Game_window("snow")
            # if the mouse is over a button but not pressed so it will stay inactive
            if self.click[0] == 0:
                self.button_aktiv = False

        # if the mouse is not over a button, so draw a button with different color
        else:
            pygame.draw.rect(self.screen, color_in_active, (x, y, width, height))
        # every button should have a centered text anyway
        text_k, text_rect = self.textObjekt(massage, self.font,(200,200,200))
        text_rect.center = ((x + (width / 2)), (y + (height / 2)))
        self.screen.blit(text_k, text_rect)
    #logo of the game
    def robo_arena_logo(self,win):
        text,text_rect = self.textObjekt("Robo Arena", font3,(200,200,200))
        win.blit(text,((self.width / 2) - text.get_width()/2, 100))
        
    #a methode to choose the weather for the map
    def chooseWeather(self):
        run = True
        while run :
            self.close_event()
            self.click = pygame.mouse.get_pressed()
            self.screen.fill((0, 0, 0))  # fill the screen with black
            self.mouse = pygame.mouse.get_pos()
            self.robo_arena_logo(self.screen)
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:  # back to the main manue by pressing Escape
                run = False
            self.button(350, 500, 300, 80, (127, 125, 125), (255, 255, 255), "snow")
            self.button(350, 600, 300, 80, (127, 125, 125), (255, 255, 255), "rain")

            self.update_screen()



