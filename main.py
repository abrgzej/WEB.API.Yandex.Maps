import sys
import os

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from gui.ui_main import Ui_MainWindow

SIZE = ["650", "450"]

class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Карты')

        self.z = 5
        self.type_map = "map"
        print("Введите координаты :")
        self.x, self.y = map(str, input().split())  # 37.530887 55.703118
        self.api_server = "http://static-maps.yandex.ru/1.x/"

        self.btn_map.clicked.connect(self.select_map_type)
        self.btn_gbr.clicked.connect(self.select_gbr_type)
        self.btn_sput.clicked.connect(self.select_sput_type)


        self.map_file = "map.png"
        self.getImage()
        self.initUI()

    def getImage(self):
        params = {
            "ll": self.x + "," + self.y,
            "z": self.z,
            "size": ",".join(SIZE),
            "l": self.type_map
        }
        response = requests.get(self.api_server, params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.pixmap = QPixmap(self.map_file)
        self.lbl_image.setPixmap(self.pixmap)

    def select_map_type(self):
        self.type_map = "map"
        self.getImage()
        self.initUI()
        self.setFocus()

    def select_gbr_type(self):
        self.type_map = "sat,skl"
        self.getImage()
        self.initUI()
        self.setFocus()

    def select_sput_type(self):
        self.type_map = "sat"
        self.getImage()
        self.initUI()
        self.setFocus()

    def keyPressEvent(self, event):
        di = {
            0: 0.0,
            1: 62.5,
            2: 62.5,
            3: 62.5,
            4: 8.5,
            5: 2.5,
            6: 1.5,
            7: 0.5,
            8: 0.3,
            9: 0.1,
            10: 0.06,
            11: 0.02,
            12: 0.012,
            13: 0.004,
            14: 0.0024,
            15: 0.0008,
            16: 0.00048,
            17: 0.00016
        }
        self.delta_x = self.delta_y = di[self.z]
        if event.key() == Qt.Key_PageUp:
            if self.z != 17:
                self.z += 1
        if event.key() == Qt.Key_PageDown:
            if self.z != 0:
                self.z -= 1
        if event.key() == Qt.Key_Up:
            if float(self.y) + self.delta_y <= 85:
                self.y = float(self.y)
                self.y += self.delta_y
                self.y = str(self.y)
        if event.key() == Qt.Key_Down:
            if float(self.y) - self.delta_y >= -85:
                self.y = float(self.y)
                self.y -= self.delta_y
                self.y = str(self.y)
        if event.key() == Qt.Key_Left:
            if float(self.x) - self.delta_x >= -180:
                self.x = float(self.x)
                self.x -= self.delta_x
                self.x = str(self.x)
        if event.key() == Qt.Key_Right:
            if float(self.x) + self.delta_x <= 180:
                self.x = float(self.x)
                self.x += self.delta_x
                self.x = str(self.x)
        self.getImage()
        self.initUI()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
