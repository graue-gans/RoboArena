import math
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
import keyboard



class BasicRobot():
    stop_thread = False

    def __init__(self, posx, posy, radius, alpha, arenawindow,color):
        self.posx = posx
        self.posy = posy
        self.direction = [1, 2]
        self.r = radius
        self.alpha = alpha
        self.color = color
        self.w = arenawindow
        self.pressedW = False
        self.pressedR = False

        self.i = 0

    def moveRobbie(self):  #dummy movement for robot1 just to show how it works.
        while not(BasicRobot.stop_thread):
            self.get_direction()

            if (self.posx + self.r == self.w.mouse[0]) and (self.posy +self.r == self.w.mouse[1]):
                self.posx = self.w.mouse[0]
                self.posy = self.w.mouse[1]
            if self.w.active:
                self.movrobot(5,5)



            self.pressedW = False
            time.sleep(0.01)

    def moveRobbie2(self):  #dummy movement for robot 2 just to show how it works.
        x = 0
        while  not(BasicRobot.stop_thread):
            self.posy = 520
            self.posx = math.sin(math.radians(2 * x)) * (500 - self.r) + 520

            time.sleep(0.01)
            x+=1
            x %= 360
            self.w.update()

    def moveRobbie3(self):
        x = 0
        while not(BasicRobot.stop_thread):
            self.posy = math.sin(math.radians(x *1)) * (500 - self.r) + 520
            self.posx = 520
            x+= 1
            x %= 360
            time.sleep(0.01)

    def moveRobbie4(self):
        self.direction = [1,2]
        while not (BasicRobot.stop_thread):
            if self.posx - self.r <= 20 :
                self.direction = [1,-2]
            if self.posx + self.r >= 1020:
                self.direction = [-2, 0]
            if self.posy - self.r <= 20:
                self.direction = [4, 1]
            if  self.posy + self.r >= 1020:
                self.direction = [-2, -3]


            self.movrobot(2,1)
            time.sleep(0.01)



                # draw the robot on the screen at its position
    def drawrobot(self,w):
        painter = QPainter(w)
        painter.setPen(QPen(QColor(self.color[0], self.color[1], self.color[2]), 8, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(self.color[0], self.color[1], self.color[2]), Qt.SolidPattern))
        painter.drawEllipse(self.posx, self.posy, self.r, self.r)
        #painter.setPen(QColor(255,255,255))
        #painter.drawArc(self.posx, self.posy, self.r, self.r, self.i * 180, 180 * 16)


    def get_direction(self):
        vector = (self.w.mouse[0] - self.posx, self.w.mouse[1] - self.posy)
        amount = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        self.direction = (1 / amount * vector[0], 1 / amount * vector[1])

    def movrobot(self,vx,vy):
        self.posx += self.direction[0] * vx
        self.posy += self.direction[1] * vy

    #rotate by using a rotation matrix
    #def rotaion(self):
       # tmep = [0,0]
      #  cos = math.cos(math.radians(self.alpha))
       # sin = math.sin(math.radians(self.alpha))
       # if abs(cos) < 0.0001:
       #     cos = 0

      #  if abs(sin) < 0.0001:
      #      sin = 0

       # tmep[0] = cos * self.direction[0] - sin * self.direction[1]
       # tmep[1] = sin * self.direction[0] + cos * self.direction[1]
      #  self.direction[0] = tmep[0]
       # self.direction[1] = tmep[1]




