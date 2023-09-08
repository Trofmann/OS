import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

import logic
from system import system
from utils import from_bytes_to_megabytes


class OS(QMainWindow):  # главное окно
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

        self.load_new_task_button = QPushButton('Загрузить новую задачу', self)
        self.load_new_task_button.move(50, 130)
        self.load_new_task_button.setFixedWidth(200)
        self.load_new_task_button.setToolTip('Загрузить новую задачу')
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

        self.speed_label = QLabel('Скорость: ', self)
        self.speed_label.move(600, 50)
        self.speed_label.setFixedWidth(300)

        self.used_memory_label = QLabel(f'Используемая память: ', self)
        self.used_memory_label.move(600, 80)
        self.used_memory_label.setFixedWidth(300)

        self.system_info_labels = [
            self.speed_label,
            self.used_memory_label
        ]

        # Изначально система не запущена, а значит информацию видеть не должны
        for label in self.system_info_labels:
            label.setVisible(False)

    @pyqtSlot()
    def start_os(self):
        if not system.is_running:
            system.tact_completed.connect(self.redraw_info_label)
            system.start()
            print('Начата работа ОС')

    @pyqtSlot()
    def load_new_task(self):
        """Загрузка новой задачи"""
        logic.load_new_task()
        print(f'Свободная память {system.get_empty_memory()} байт')

    @pyqtSlot()
    def increase_speed(self):
        system.increase_speed()
        print(f'{system.speed} миллисекунд на тик')

    @pyqtSlot()
    def decrease_speed(self):
        system.decrease_speed()
        print(f'{system.speed} миллисекунд на тик')

    @pyqtSlot()
    def change_input_data(self):
        print('Изменение входных данных')

    @pyqtSlot()
    def redraw_info_label(self):
        self.speed_label.setText(f'Скорость: {system.speed} миллисекунд на тик')
        self.speed_label.setVisible(True)

        used_memory = from_bytes_to_megabytes(system.get_used_memory())

        self.used_memory_label.setText(f'Используемая память: {used_memory} МБ')
        self.used_memory_label.setVisible(True)

    @pyqtSlot()
    def stop_modeling(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OS()
    ex.show()
    sys.exit(app.exec_())
