import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *


class OS(QWidget):  # главное окно
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setStyleSheet("background-color: #d3d3d3;")
        self.setWindowTitle("OS")  # заголовок окна
        self.move(300, 300)  # положение окна
        self.resize(1000, 600)  # размер окна

        self.manage_commands_label = QLabel('Команды управления', self)
        self.manage_commands_label.move(50, 50)
        self.manage_commands_label.setFixedWidth(200)

        self.init_os_button = QPushButton('Начать работу ОС', self)
        self.init_os_button.move(50, 100)
        self.init_os_button.setFixedWidth(200)
        self.init_os_button.setToolTip('Начать работу ОС')
        self.init_os_button.clicked.connect(self.start_os)

        self.load_new_task_button = QPushButton('Загрузить новое задание', self)
        self.load_new_task_button.move(50, 130)
        self.load_new_task_button.setFixedWidth(200)
        self.load_new_task_button.setToolTip('Загрузить новое задание')
        self.load_new_task_button.clicked.connect(self.load_new_task)

        self.increase_speed_button = QPushButton('Увеличить скорость ОС', self)
        self.increase_speed_button.move(50, 160)
        self.increase_speed_button.setFixedWidth(200)
        self.increase_speed_button.setToolTip('Увеличить скорость ОС')
        self.increase_speed_button.clicked.connect(self.increase_speed)

        self.decrease_speed_button = QPushButton('Уменьшить скорость ОС', self)
        self.decrease_speed_button.move(50, 190)
        self.decrease_speed_button.setFixedWidth(200)
        self.decrease_speed_button.setToolTip('Уменьшить скорость ОС')
        self.decrease_speed_button.clicked.connect(self.decrease_speed)

        self.change_input_data_button = QPushButton('Изменить входные данные', self)
        self.change_input_data_button.move(50, 220)
        self.change_input_data_button.setFixedWidth(200)
        self.change_input_data_button.setToolTip('Изменить входные данные')
        self.change_input_data_button.clicked.connect(self.change_input_data)

        self.stop_modeling_button = QPushButton('Завершить моделирование', self)
        self.stop_modeling_button.move(50, 250)
        self.stop_modeling_button.setFixedWidth(200)
        self.stop_modeling_button.setToolTip('Завершить моделирование')
        self.stop_modeling_button.clicked.connect(self.stop_modeling)

    @pyqtSlot()
    def start_os(self):
        print('Начата работа ОС')

    @pyqtSlot()
    def load_new_task(self):
        print('Загрузка нового задания')

    @pyqtSlot()
    def increase_speed(self):
        print('Увеличение скорости')

    @pyqtSlot()
    def decrease_speed(self):
        print('Уменьшение скорости')

    @pyqtSlot()
    def change_input_data(self):
        print('Изменение входных данных')

    @pyqtSlot()
    def stop_modeling(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OS()
    sys.exit(app.exec_())
