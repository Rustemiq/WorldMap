import os
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, \
    QLineEdit
from PyQt6.QtCore import Qt

from get_map import get_map
from get_obj_info import get_obj_info

SCREEN_SIZE = (1000, 500)
map_file = 'map.png'
spn_up_limit = 2.3
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
        self.resetButton = QPushButton('Сброс поиска', self)
        self.resetButton.move(600, 90)
        self.resetButton.clicked.connect(self.reset)
        self.addressLine = QLineEdit('Адрес', self)
        self.addressLine.setEnabled(False)
        self.addressLine.move(600, 130)
        self.addressLine.resize(400, 20)
        self.postalButton = QPushButton('Почт. инд.: вкл', self)
        self.postalButton.move(600,  180)
        self.postalButton.clicked.connect(self.switchPostalCodeVisible)
        self.is_postal_code_visible = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.cur_spn += 1
        elif event.key() == Qt.Key.Key_PageDown:
            self.cur_spn -= 1
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

    def writeAddress(self, address, postal_code):
        if postal_code is not None and self.is_postal_code_visible:
            address += ', Почт. инд.:' + postal_code
        self.addressLine.setText(address)

    def search(self):
        try:
            self.cur_ll, address, postal_code = get_obj_info(self.searchLine.text())
            self.cur_pt = self.cur_ll[:]
            self.writeAddress(address, postal_code)
            self.updateMap()
        except IndexError:
            self.searchLine.setText('Не найдено')
        except KeyError:
            pass

    def reset(self):
        self.cur_pt = None
        self.searchLine.setText('')
        self.addressLine.setText('Адрес')
        self.updateMap()

    def switchPostalCodeVisible(self):
        self.is_postal_code_visible = not self.is_postal_code_visible
        self.postalButton.setText(
            'Почт. инд.: вкл' if self.postalButton.text() == 'Почт. инд.: выкл' else 'Почт. инд.: выкл'
        )
        address, postal_code = get_obj_info(self.searchLine.text())[1:]
        self.writeAddress(address, postal_code)

    def closeEvent(self, event):
        os.remove(map_file)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec())