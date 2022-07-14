from PyQt5.QtWidgets import QWidget, QPushButton  # only import necessary modules 


class MainMenu(QWidget):
    """
    MainMenu class extends QWidget and is always called upon starting the game
    """

    def __init__(self, width, height):
        pass

    def initUI(self):
        pass

class MenuButton(QPushButton):
    """
    MenuButton class extends QPushButton
    Is used to create different buttons for the main menu
    """

    def __init__(self, function, text, window):
        pass
