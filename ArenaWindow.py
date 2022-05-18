import sys
import threading
import time


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
        self.initialBackground(self.windowSizeTiles, 13, 2)
        self.printBackground()



    def initArenaWindow(self):
        self.setFixedSize(self.arenaSizeinPx, self.arenaSizeinPx)
        self.setWindowTitle("Robo-Arena-Team")
        self.spawnRobot()
        self.show()



    def spawnRobot(self):
        Robbie = BasicRobot((500, 500), 4, 135)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(Robbie.color[0], Robbie.color[1], Robbie.color[2]), 8, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(Robbie.color[0], Robbie.color[1], Robbie.color[2]), Qt.SolidPattern))
        painter.drawEllipse(Robbie.pos[0], Robbie.pos[1], Robbie.r, Robbie.r)

    #each number in this 2-d list represent a diffrent tile
    def initialBackground(self, arenasizeTiles, wallsize, wattersize):
        for i in range(arenasizeTiles):
            self.background.append([])
            for j in range(arenasizeTiles):
                if (i < wallsize or i >= arenasizeTiles - wallsize) or (j < wallsize or j >= arenasizeTiles - wallsize):
                    self.background[i].append(0)#0 for green
                elif (i < wallsize + wattersize or i >= arenasizeTiles - wallsize - wattersize) or (
                        j < wallsize + wattersize or j >= arenasizeTiles - wallsize - wattersize):
                    self.background[i].append(1)#1 for red
                else:
                    self.background[i].append(2)# for yellow


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawtiles(qp)
        qp.end()

    #drow the tiles from the 2-d-background-list
    def drawtiles(self, qp):
        for i in range(self.windowSizeTiles):
            for j in range(self.windowSizeTiles):

                if self.background[i][j] == 0:
                    self.a ='#2ABF0F'
                    qp.setPen(QColor(self.a))
                    qp.setBrush(QColor(self.a))
                    qp.drawRect(i*self.tilesize,j*self.tilesize, 10, 10)

                elif self.background[i][j] == 1:
                    self.a ='#E03434'
                    qp.setPen(QColor(self.a))
                    qp.setBrush(QColor(self.a))
                    qp.drawRect(i * self.tilesize, j * self.tilesize, 10, 10)

                else:
                    self.a = '#D4F52F'
                    qp.setPen(QColor(self.a))
                    qp.setBrush(QColor(self.a))
                    qp.drawRect(i * self.tilesize, j * self.tilesize, 10, 10)


    def updatemap(self): #update the map in a infinit loop, to be able to have an interactive arena. Active the Thread in Mainwindow!
        while True:
            for i in range(self.windowSizeTiles):
                for j in range(self.windowSizeTiles):
                    self.update()



    #to keep an eye on the backgroundlist
    def printBackground(self):
        for i in range(self.windowSizeTiles):
            for j in range(self.windowSizeTiles):
                print(self.background[i][j], end=" ")
            print()










