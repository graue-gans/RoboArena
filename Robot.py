import math
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter
import keyboard
import time


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
        self.v = [1,1]
        self.pressedW = False
        self.pressedR = False
        self.running = 0
        self.not_running = 0
        self.pressedwr = False


        self.i = 0

    def moveRobbie(self):  #dummy movement for robot1 just to show how it works.
        counter = 0
        start = 0
        while not(BasicRobot.stop_thread):
            self.get_direction()

            if (self.posx <= self.w.mouse[0] + self.r and self.posx > self.w.mouse[0] - self.r) and (self.posy<= self.w.mouse[1] + self.r and self.posy > self.w.mouse[1] - self.r):
                self.w.active = False
            if self.w.active:

                self.get_direction()
                self.movrobot()





            counter += 1
            counter %= 100
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
        counter = 0
        running = False

        while not (BasicRobot.stop_thread):
            print("1")
            if keyboard.is_pressed('w'):
                print("max")
                self.running += 1
                self.not_running = 0
                self.get_v()
                self.movrobot()
            else:
                self.not_running += 1
                self.stopping()
                self.movrobot()
            #print(self.v[0], self.v[1])









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
        self.direction = [1 / amount * vector[0], 1 / amount * vector[1]]

    def stopping(self):
        if self.v[0] - (1 / 2 * (self.not_running / 100) ** 2 ) > 0 and  self.v[1] - (1 / 2 + (self.not_running / 100) ** 2 ) >0:
            self.v[0] = self.v[0] - (1 / 2 * (self.not_running / 100) ** 2 * 0.5)
            self.v[1] = self.v[1] - (1 / 2 + (self.not_running / 100) ** 2  * 0.5)
        else:
            self.running = 0
            self.v[0] = 0
            self.v[1] = 0


    def movrobot(self):
            self.posx += self.direction[0] * self.v[0]
            self.posy += self.direction[1] * self.v[1]


    def get_v(self):
        if self.running != 0 :
            self.v[0]= (1/2 * (self.running/100) ** 2 )
            self.v[1]= (1/2 + (self.running/100) ** 2 )

    def keyboardListener(self) :
        while not(BasicRobot.stop_thread):
           if keyboard.read_key() == 'w' and keyboard.read_key() == 'r':
               self.pressedwr = True
               print("peter")
           if keyboard.read_key() == 'w':
               self.pressedW= True

           if keyboard.read_key() == 'r':
               self.pressedR = True



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




