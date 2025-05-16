import os
import sys
import math

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, \
    QLineEdit
from PyQt6.QtCore import Qt

from get_map import get_map
from get_obj_info import get_obj_info
from get_organization import get_org

SCREEN_SIZE = (1000, 500)
map_file = 'map.png'
spn_up_limit = 2.3
spn_down_limit = 0.3
lat_up_limit, lat_down_limit = 85, -85
map_left_top = 0, 0


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cur_ll = [20, 40]
        self.cur_spn = spn_down_limit
        self.cur_pt = None
        self.address = 'Адрес'
        self.postal_code = None
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

    def writeAddress(self):
        full_address = self.address
        if self.postal_code is not None and self.is_postal_code_visible:
            full_address += ', Почт. инд.:' + self.postal_code
        self.addressLine.setText(full_address)

    def search(self):
        try:
            ll, self.address, self.postal_code = get_obj_info(self.searchLine.text())
            self.cur_pt = ll[:]
            self.cur_ll = ll[:]
            self.writeAddress()
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
        self.writeAddress()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x, y = event.pos().x() - map_left_top[0], event.pos().y() - map_left_top[1]
            left, top = self.cur_ll[0] - self.cur_spn, self.cur_ll[1] + self.cur_spn
            lon = left + self.cur_spn * 2 * (x / 600)
            lat = top - self.cur_spn * 2 * (y / 450)
            self.address, self.postal_code = get_obj_info(str(lon) + ',' + str(lat))[1:]
            self.cur_pt = [lon, lat]
            self.writeAddress()
            self.updateMap()
        if event.button() == Qt.MouseButton.RightButton:
            x, y = event.pos().x() - map_left_top[0], event.pos().y() - map_left_top[1]
            left, top = self.cur_ll[0] - self.cur_spn, self.cur_ll[1] + self.cur_spn
            lon = left + self.cur_spn * 2 * (x / 600)
            lat = top - self.cur_spn * 2 * (y / 450)
            org_name = self.searchLine.text()
            pt, address = get_org(str(lon) + ',' + str(lat), org_name)
            self.cur_pt = pt if pt else self.cur_pt
            self.address = address if address else self.address

            self.updateMap()
            self.writeAddress()

    def closeEvent(self, event):
        os.remove(map_file)

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec())