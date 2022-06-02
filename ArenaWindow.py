import csv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QPainter, QBrush, QPen, QColor
from Robot import BasicRobot
import keyboard
import time





class ArenaWindow(QMainWindow):
    def __init__(self, arenaSizeinPx,window):
        window.hide()
        self.arenaSizeinPx = arenaSizeinPx
        self.windowSizeTiles = int(self.arenaSizeinPx / 10)
        self.tilesize = 10
        super().__init__()
        self.initArenaWindow()
        self.background = []
        self.wallsize = 2
        self.initialBackground(self.windowSizeTiles, self.wallsize)
        self.Robbie = BasicRobot(200, 250, 20, 90,self,(81, 63, 167))
        self.Robbie2 = BasicRobot(800, 500, 20, 135,self,(255, 1, 1))
        self.Robbie3 = BasicRobot(800, 200, 20, 135,self,(255, 255, 255))
        self.Robbie4 = BasicRobot(100, 100, 20, 135,self,(101, 191, 101))
        self.mouse = [0,0]
        self.loadbackground()
        self.active = False



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
        qp = QPainter()
        qp.begin(self)
        self.drawtiles(qp)
        self.Robbie.drawrobot(self)
        self.Robbie2.drawrobot(self)
        self.Robbie3.drawrobot(self)
        self.Robbie4.drawrobot(self)
        #self.reset()   #reset the background

        qp.end()

    def keyboardListener(self) :
        while not(BasicRobot.stop_thread):
            if keyboard.read_key() == 'w':
                self.Robbie.pressedW = True
            if keyboard.read_key() == 'r':
                self.Robbie.pressedR = True




    def mousePressEvent(self, event):
        self.mouse = (event.x(),event.y())
        self.active = True
        if event.button() == Qt.LeftButton:
            self.active = False


    #draw a single tile with Qpainter
    def drawTile(self,qp,color,i,j):
        qp.setBrush(QColor(color))
        qp.drawRect(i * self.tilesize, j * self.tilesize, 10, 10)

    #Kill the threads by closing the window
    def closeEvent(self, e):
       BasicRobot.stop_thread = True
       self.close()


    #draw the tiles depending on the number of it
    def drawtiles(self, qp):
        for i in range(self.windowSizeTiles):
            for j in range(self.windowSizeTiles):


                if self.background[i][j] == 0:          #wall
                    qp.setPen(QColor('#ffffff'))
                    self.drawTile(qp,'#633E3E',i,j)

                elif self.background[i][j] == 1:        #sand
                    qp.setPen(Qt.NoPen)
                    self.drawTile(qp,'#Eff18a',i,j)

                elif self.background[i][j] == 2: #green
                    qp.setPen(Qt.NoPen)
                    self.drawTile(qp, '#1D1A1A', i, j)
                    #qp.setPen(Qt.NoPen)
                   # self.drawTile(qp,'#0a7107',i,j)

                elif self.background[i][j] == 3:        #rot
                    qp.setPen(QColor('#000000'))
                    self.drawTile(qp,'#901152',i,j)

                elif self.background[i][j] == 4:        #schwarz
                    qp.setPen(Qt.NoPen)
                    self.drawTile(qp,'#1D1A1A',i,j)

                elif self.background[i][j] == 5:        #grau
                    qp.setPen(Qt.NoPen)
                    self.drawTile(qp,'#AFA9A9',i,j)

                elif self.background[i][j] == 6:        #blau
                    qp.setPen(Qt.NoPen)
                    self.drawTile(qp,'#1B29D4',i,j)

                elif self.background[i][j] == 7:        #oil
                    qp.setPen(Qt.NoPen)
                    self.drawTile(qp,'#3e3f01',i,j)         


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