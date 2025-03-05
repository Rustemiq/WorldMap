import os
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, \
    QLineEdit
from PyQt6.QtCore import Qt

from get_map import get_map
from get_coord import get_coord

SCREEN_SIZE = [800, 500]
map_file = 'map.png'
spn_up_limit = 1.8
spn_down_limit = 0.3
lat_up_limit, lat_down_limit = 85, -85


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cur_ll = [20, 40]
        self.cur_spn = spn_down_limit
        self.cur_pt = None
        self.initUI()
        self.updateMap()

    def updateMap(self):
        get_map(self.cur_ll, self.cur_spn, self.cur_pt, self.theme)
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
        self.themeChanger = QPushButton('Тема: светлая', self)
        self.themeChanger.move(650, 0)
        self.themeChanger.clicked.connect(self.changeTheme)
        self.theme = 'light'
        self.searchLine = QLineEdit(self)
        self.searchLine.move(600, 50)
        self.searchButton = QPushButton('Искать', self)
        self.searchButton.move(720, 50)
        self.searchButton.clicked.connect(self.search)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.cur_spn += 0.7
        elif event.key() == Qt.Key.Key_PageDown:
            self.cur_spn -= 0.7
        if self.cur_spn < spn_down_limit:
            self.cur_spn = spn_down_limit
        if self.cur_spn > spn_up_limit:
            self.cur_spn = spn_up_limit
        if event.key() == Qt.Key.Key_S:
            self.cur_ll[1] -= self.cur_spn / 2
        if event.key() == Qt.Key.Key_W:
            self.cur_ll[1] += self.cur_spn / 2
        if event.key() == Qt.Key.Key_D:
            self.cur_ll[0] += self.cur_spn / 2
        if event.key() == Qt.Key.Key_A:
            self.cur_ll[0] -= self.cur_spn / 2
        if self.cur_ll[1] < lat_down_limit:
            self.cur_ll[1] = lat_down_limit
        if self.cur_ll[1] > lat_up_limit:
            self.cur_ll[1] = lat_up_limit
        self.cur_ll[0] = (self.cur_ll[0] + 180) % 360 - 180

        self.updateMap()

    def changeTheme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.themeChanger.setText(
            'Тема: светлая' if self.themeChanger.text() == 'Тема: темная' else 'Тема: темная'
        )
        self.updateMap()

    def search(self):
        try:
            self.cur_ll = get_coord(self.searchLine.text())
            self.cur_pt = self.cur_ll[:]
            self.updateMap()
        except IndexError:
            self.searchLine.setText('Не найдено')
        except KeyError:
            pass

    def closeEvent(self, event):
        os.remove(map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec())