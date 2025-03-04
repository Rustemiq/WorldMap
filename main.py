import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QTextEdit

from get_map import get_map

SCREEN_SIZE = [800, 500]
map_file = 'map.png'


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def updateMap(self, ll, spn):
        get_map(ll, spn)
        self.pixmap = QPixmap(map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('WorldMap')

        self.pixmap = QPixmap(map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = MainWindow()
    wind.show()

    #test
    wind.updateMap('30,35', '5,5')

    sys.exit(app.exec())