import os
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt

from get_map import get_map

SCREEN_SIZE = [800, 500]
map_file = 'map.png'
spn_limit = 1.8
spn_min = 0.3


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cur_ll = [30, 50]
        self.cur_spn = spn_min
        self.initUI()
        self.updateMap()

    def updateMap(self):
        get_map(self.cur_ll, self.cur_spn)
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.cur_spn += 0.7
        elif event.key() == Qt.Key.Key_PageDown:
            self.cur_spn -= 0.7
        if self.cur_spn < spn_min:
            self.cur_spn = spn_min
        if self.cur_spn > spn_limit:
            self.cur_spn = spn_limit
        self.updateMap()

    def closeEvent(self, event):
        os.remove(map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec())