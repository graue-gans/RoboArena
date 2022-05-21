import sys
import threading
import time
import csv


from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QPainter, QBrush, QPen, QColor, QLinearGradient, QPixmap
from Robot import BasicRobot
from PyQt5 import QtCore, QtGui, QtWidgets
from ArenaButton import ArenaButton
import threading



class ArenaWindow(QMainWindow):
    def __init__(self, arenaSizeinPx,window):
        window.hide()
        self.arenaSizeinPx = arenaSizeinPx
        self.windowSizeTiles = int(self.arenaSizeinPx / 10)
        self.tilesize = 10
        super().__init__()
        self.initArenaWindow()
        self.background = []
        self.wallsize = 4
        self.initialBackground(self.windowSizeTiles, self.wallsize)
        self.Robbie = BasicRobot(500, 500, 20, 135)





    def initArenaWindow(self):
        self.setFixedSize(self.arenaSizeinPx, self.arenaSizeinPx)
        self.setWindowTitle("Robo-Arena-Team")
        self.show()




    def drowrobot (self,qp):
        #painter = QPainter(self)
        qp.setPen(QPen(QColor(self.Robbie.color[0], self.Robbie.color[1], self.Robbie.color[2]), 8, Qt.SolidLine))
        qp.setBrush(QBrush(QColor(self.Robbie.color[0], self.Robbie.color[1], self.Robbie.color[2]), Qt.SolidPattern))
        qp.drawEllipse(self.Robbie.posx, self.Robbie.posy, self.Robbie.r, self.Robbie.r)

    def moveRobbie(self):
        count = 1
        richtung = (4,4) #dummy just to show how it works.
        while(1):
            for i in range(self.arenaSizeinPx):
                if self.Robbie.posx + 150 + self.Robbie.r >= self.arenaSizeinPx:
                    richtung = (-2, -2)

                elif self.Robbie.posx - 150 - self.Robbie.r <= 0:
                    richtung = (2, 2)

                self.Robbie.posx += richtung[0]
                self.Robbie.posy += richtung[1]
                time.sleep(0.01)
                self.update()

    def drawInformation(self,robot):
        l1robot1 = QLabel("Robot")
        l1robot1.setGeometry(0,0,200,50)







#initialize the background, each number in the list is a tile
    def initialBackground(self, arenasizeTiles, wallsize):
        for i in range(arenasizeTiles):
            self.background.append([])
            for j in range(arenasizeTiles):
                if (i < wallsize or i >= arenasizeTiles - wallsize) or (j < wallsize or j >= arenasizeTiles - wallsize):
                    self.background[i].append(0)
                else:
                    self.background[i].append(2)


    def paintEvent(self, e):
        self.loadbackground()
        qp = QPainter()
        qp.begin(self)
        self.drawtiles(qp)
        self.drowrobot(qp)
        #self.savebackground() #save the background

        qp.end()

    #draw a tile with paintevent
    def drawTile(self,qp,color,i,j):
        qp.setBrush(QColor(color))
        qp.drawRect(i * self.tilesize, j * self.tilesize, 10, 10)

    def closeEvent(self, e):
       self.t.close()
       self.close()

    def set_t(self,t):
        self.t = t



    #draw the tiles
    def drawtiles(self, qp):
        for i in range(self.windowSizeTiles):
            for j in range(self.windowSizeTiles):


                if self.background[i][j] == 0: #wall
                    qp.setPen(QColor('#ffffff'))
                    self.drawTile(qp,'#633E3E',i,j)

                elif self.background[i][j] == 3:
                    qp.setPen(QColor('#000000'))
                    self.drawTile(qp,'#901152',i,j)

                elif self.background[i][j] == 4:
                    qp.setPen(Qt.NoPen)
                    self.drawTile(qp,'#1D1A1A',i,j)

                elif self.background[i][j] == 5:
                    qp.setPen(QColor('#000000'))
                    self.drawTile(qp,'#AFA9A9',i,j)

                elif self.background[i][j] == 6:
                    qp.setPen(Qt.NoPen)
                    self.drawTile(qp,'#1B29D4',i,j)

                else:
                    qp.setPen(Qt.NoPen)  #arena
                    self.drawTile(qp,'#000000' ,i,j)








    def savebackground(self):
        with open('background.csv', 'w', encoding='UTF8',newline='') as f:
            firstline = True
            writer = csv.writer(f)
            for i in range(len(self.background)):
                    writer.writerow(self.background[i])
        f.close()

    def loadbackground(self):
        file = open('background.csv')
        csvreader = csv.reader(file)
        rows = []
        for row in csvreader:
            rows.append(row)

        for i in range(len(rows)):
            for j in range(len(rows[i])):
                self.background[j][i] = int(rows[i][j])
        file.close()









    def updatemap(self): #update the map in a infinit loop, to be able to have an interactive arena. Active the Thread in Mainwindow!
        while True:
            for i in range(self.windowSizeTiles):
                for j in range(self.windowSizeTiles):
                    self.update()



    #to keep an eye on the backgroundlist
    #def printBackground(self):
        #for i in range(self.windowSizeTiles):
           # for j in range(self.windowSizeTiles):
              #  print(self.background[i][j], end=" ")
           # print()










