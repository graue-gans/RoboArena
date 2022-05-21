import sys
import threading
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy, QMenu
from PyQt5 import QtCore, QtMultimedia, QtMultimediaWidgets,QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPalette, QBrush, QMovie, QPainter, QPixmap

from ArenaButton import ArenaButton
from ArenaWindow import ArenaWindow



class Window(QWidget):


    def __init__(self,windowWidth,windowHeight):
        self.w = None
        self.windowwidth = windowWidth
        self.windowHeight = windowHeight
        super().__init__()
        self.initUI()


    def initUI(self):
        exitbutton = ArenaButton("exitbutton","exit",self)
        playbutton = ArenaButton("playbutton","play", self)
        settingbutton = ArenaButton("settingbutton","setting", self)
        playbutton.clicked.connect(self.arenaWindowCall)
        exitbutton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.l1 = QLabel('Robo Arena',self)
        self.l1.setStyleSheet(
            "font-size:100px;"
            "font-style: oblique;"
            "font-weight: 900;"
            "font-variant: small-caps;"
            "color:black;"
        )
        oImage = QImage("robotpic.png")
        sImage = oImage.scaled(QSize(self.windowwidth, self.windowHeight))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.setFixedSize(self.windowwidth,self.windowHeight)
        self.setWindowTitle("Robo-Arena-Team")
        self.show()

    def arenaWindowCall(self):
        self.w = ArenaWindow(1040, self)
        t = threading.Thread(target=self.w.moveRobbie,args=()) #thread1 for robot1
        t2 = threading.Thread(target=self.w.moveRobbie2, args=())  # thread1 for robot1
        t.start()
        t2.start()
        self.w.set_thread_1 = t















app = QApplication(sys.argv)
w = Window(1920,1080)

sys.exit(app.exec_())


