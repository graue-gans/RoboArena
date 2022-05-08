# import necessary packages
import sys
from PyQt5.QtWidgets import QApplication, QWidget


def main():

    # create app object
    app = QApplication(sys.argv)

    w = QWidget()  # create window
    w.resize(250, 150)  # in 1 px
    w.move(300, 300)
    w.setWindowTitle('RoboArena')
    
    # show window on screen
    w.show()

    # enter mainloop and ensure clean exit if window is destroyed or exited
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
