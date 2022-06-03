from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import sys
import getData
from gl import *


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("GUI.ui", self)

        self.glWidget = GLWidget(self.graphic)

        self.glWidget.setRotX(45, self.gyro_1)
        self.glWidget.setRotY(45, self.gyro_2)
        self.glWidget.setRotZ(45, self.gyro_3)

        timer = QtCore.QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()


def main():
    data = getData
    app = QApplication(sys.argv)
    win = UI()
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
