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
        print("Введите координаты :")
        self.x, self.y = map(str, input().split())  # 37.530887 55.703118
        self.api_server = "http://static-maps.yandex.ru/1.x/"


        self.map_file = "map.png"
        self.getImage()
        self.initUI()

    def getImage(self):
        params = {
            "ll": self.x + "," + self.y,
            "z": self.z,
            "size": ",".join(SIZE),
            "l": "map"
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.z != 17:
                self.z += 1
        if event.key() == Qt.Key_PageDown:
            if self.z != 0:
                self.z -= 1
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
