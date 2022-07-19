import pygame

_WINDOW_WIDTH = 1000
_WINDOW_HEIGHT = 1000
_WINDOW_TITLE = 'RoboArena'


class Screen():

    """
    Main class for the RoboArena game
    It holds outside parameters and the game window itself
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # self.title  = title
        self.init_main_menu()

    def init_main_menu(self):
        # initialize the main menu (which is our starting screen)
        # ...
        # return window
        # main_menu = Main_menu()
        print("hey")

    # other methods: init_x_window, ...


if __name__ == "__main__":
    s = Screen(_WINDOW_WIDTH, _WINDOW_HEIGHT)
