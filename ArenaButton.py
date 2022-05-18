import sys
from PyQt5.QtWidgets import QPushButton, QMenu
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QMargins


class ArenaButton(QPushButton):
    counter = 0
    distance = 0
    setting_menu = [
        {'FPS': ['50', '80', '100', '200']},
        {'LEVEL': ['Easy', 'Normal', 'Hard']}]

    def __init__(self,name,text,window):
        self.name = name
        ArenaButton.counter += 1
        super().__init__(text,window)
        self.placeButton(window)
        self.stylebutton(window)
        self.anim = QPropertyAnimation(self, b'geometry')
        self.anim.setDuration(1000)
        self.anim.setEasingCurve(QEasingCurve.OutElastic)
        self.initSettingMenu(window)


    @staticmethod
    def buttonSizeX(window):
        return int(window.windowwidth/5)
    @staticmethod
    def buttonSizeY(window):
        return int(window.windowHeight/10)

    def startPostionX(self,window):
            if ArenaButton.counter==1:
                ArenaButton.distance = (ArenaButton.buttonSizeX(window)/2)
                return ArenaButton.distance
            else:
                ArenaButton.distance += ArenaButton.buttonSizeX(window) + window.windowwidth *(1/10)
                return ArenaButton.distance
    def startPositionY(self,window):
        return int(window.windowHeight - ArenaButton.buttonSizeY(window)*2)

    def enterEvent(self,event):
            self.anim.setDirection(self.anim.Forward)
            if self.anim.state() == self.anim.State.Stopped:
                rect = self.geometry()
                self.anim.setStartValue(rect)
                rect+=QMargins(10,10,10,10)
                if(self.name == "exitbutton"):
                    rect.translate(-20, 20)
                elif(self.name == "playbutton"):
                    rect.translate(0, -20)
                elif (self.name == "settingbutton"):
                    rect.translate(20, 20)


                self.anim.setEndValue(rect)
                self.anim.start()
            QPushButton.enterEvent(self, event)

    def leaveEvent(self,event):
        self.anim.setDirection(self.anim.Backward)
        if self.anim.state() == self.anim.State.Stopped: self.anim.start()
        QPushButton.leaveEvent(self,event)

    def stylebutton(self,window):
        self.setStyleSheet("""
             QWidget {
                    border: 10px solid #3F3E2F;
                    border-radius: 2em;
                    background-color: #BBB765;
                    font:20px;
                
                     }
                QPushButton:hover
                    {
                    border: 10px solid grey;
                    background-color: #FFFFCC;
                    }
                QPushButton:pressed
                    {
                    background-color: #EAE79F;     
                    }
                    """)




    def placeButton(self,window):
         self.setGeometry(int(self.startPostionX(window)), int(self.startPositionY(window)), int(ArenaButton.buttonSizeX(window)), int(ArenaButton.buttonSizeY(window)))

    def initSettingMenu(self,window):
        if(self.name=="settingbutton"):
            menu = QMenu()

            self.setMenu(menu)
            self.add_menu(ArenaButton.setting_menu,menu)
            menu.setStyleSheet("""
             QWidget {
                    border: 4px solid #3F3E2F;
                    border-radius: 10px;
                    background-color: #BBB765;
                    font:20px;
                     }
                    """)
            menu.setFixedSize(ArenaButton.buttonSizeX(window),ArenaButton.buttonSizeY(window))

    def add_menu(self,data,menu_obj):
        if isinstance(data, dict):
            for k, v in data.items():
                sub_menu = QMenu(k, menu_obj)
                menu_obj.addMenu(sub_menu)
                self.add_menu(v, sub_menu)
        elif isinstance(data, list):
            for element in data:
                self.add_menu(element, menu_obj)
        else:
            action = menu_obj.addAction(data)
            action.setIconVisibleInMenu(False)
















