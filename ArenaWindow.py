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
        self.Robbie = BasicRobot(500, 500, 20, 135,self)
        self.Robbie2 = BasicRobot(300, 300, 20, 135,self)
        self.Robbie3 = BasicRobot(200, 200, 20, 135,self)
        self.Robbie4 = BasicRobot(100, 100, 20, 135,self)


    def initArenaWindow(self):
        self.setFixedSize(self.arenaSizeinPx, self.arenaSizeinPx)
        self.setWindowTitle("Robo-Arena-Team")
        self.show()


#initialize the background, each number in the list is a tile
    def initialBackground(self, arenasizeTiles, wallsize):
        for i in range(arenasizeTiles):
            self.background.append([])
            for j in range(arenasizeTiles):
                if (i < wallsize or i >= arenasizeTiles - wallsize) or (j < wallsize or j >= arenasizeTiles - wallsize):
                    self.background[i].append(0)
                else:
                    self.background[i].append(2)

    #has its own thread, is aktiv when ever we update or change the window
    def paintEvent(self, e):
        self.loadbackground()
        qp = QPainter()
        qp.begin(self)
        self.drawtiles(qp)
        self.Robbie.drawrobot(self,qp)
        self.Robbie2.drawrobot(self,qp)
        #self.reset() #reset the background

        qp.end()

    #draw a single tile with Qpainter
    def drawTile(self,qp,color,i,j):
        qp.setBrush(QColor(color))
        qp.drawRect(i * self.tilesize, j * self.tilesize, 10, 10)

    #Kill the threads by closing the window
    def closeEvent(self, e):
       self.Robbie.stop_thread = True
       self.Robbie2.stop_thread = True
       self.close()


    #draw the tiles depending on the number of it
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

#inialize the background
    def reset(self):
        with open('background.csv', 'w', encoding='UTF8',newline='') as f:
            firstline = True
            writer = csv.writer(f)
            for i in range(len(self.background)):
                    writer.writerow(self.background[i])
        f.close()

#load the background from a csv-data
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



    #to keep an eye on the backgroundlist
    #def printBackground(self):
        #for i in range(self.windowSizeTiles):
           # for j in range(self.windowSizeTiles):
              #  print(self.background[i][j], end=" ")
           # print()