import time

from PyQt5.QtGui import QBrush, QPen, QColor

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QPainter, QBrush, QPen, QColor, QLinearGradient, QPixmap



class BasicRobot():
    def __init__(self, posx, posy, radius, alpha, arenawindow):
        self.posx = posx
        self.posy = posy
        self.r = radius
        self.alpha = alpha
        self.color = (81, 63, 167)
        self.w = arenawindow
        self.stop_thread = False

    def moveRobbie(self):#dummy movement for robot1 just to show how it works.
        richtung = (2, 1)
        while True:

            if self.stop_thread:
                break
            for i in range(self.w.arenaSizeinPx):
                if self.stop_thread:
                    break
                if self.w.Robbie.posx + 40 + self.w.Robbie.r >= self.w.arenaSizeinPx or self.w.Robbie.posy + 40 + self.w.Robbie.r >= self.w.arenaSizeinPx:
                    richtung = (-4, -2)

                elif self.w.Robbie.posx - 40 - self.w.Robbie.r <= 0 or self.w.Robbie.posy - 40 - self.w.Robbie.r <= 0:
                    richtung = (10, 2)
                self.w.Robbie.posx += richtung[0]
                self.w.Robbie.posy += richtung[1]
                time.sleep(0.01)
                self.w.update()


    def moveRobbie2(self):#dummy movement for robot 2 just to show how it works.
        richtung = (2,1)
        while True:

            if self.stop_thread:
                break
            for i in range(self.w.arenaSizeinPx):
                if self.stop_thread:
                    break
                if self.w.Robbie2.posx + 40 + self.w.Robbie2.r >= self.w.arenaSizeinPx or self.w.Robbie2.posy + 40 + self.w.Robbie2.r >= self.w.arenaSizeinPx:
                    richtung = (-4, -2)

                elif self.w.Robbie2.posx - 40 - self.w.Robbie2.r <= 0 or self.w.Robbie2.posy - 40 - self.w.Robbie2.r <= 0:
                    richtung = (10, 2)
                self.w.Robbie2.posx += richtung[0]
                self.w.Robbie2.posy += richtung[1]
                time.sleep(0.01)
                self.w.update()

    # draw the robot on the screen at its position
    def drawrobot(self,w, qp):
        # painter = QPainter(self)
        qp.setPen(QPen(QColor(self.color[0], self.color[1], self.color[2]), 8, Qt.SolidLine))
        qp.setBrush(QBrush(QColor(self.color[0], self.color[1], self.color[2]), Qt.SolidPattern))
        qp.drawEllipse(self.posx, self.posy, self.r, self.r)