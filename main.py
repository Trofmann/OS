import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from collections import deque

import logic
from system import system
from utils import from_bytes_to_megabytes, from_megabytes_to_bytes


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

        self.stop_modeling_button = QPushButton('Завершить моделирование', self)
        self.stop_modeling_button.move(50, 220)
        self.stop_modeling_button.setFixedWidth(200)
        self.stop_modeling_button.setToolTip('Завершить моделирование')
        self.stop_modeling_button.clicked.connect(self.stop_modeling)

        self.set_system_button_disabled(True)

        self.exit_button = QPushButton('Выйти', self)
        self.exit_button.move(50, 250)
        self.exit_button.setFixedWidth(200)
        self.exit_button.setToolTip('Выйти')
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setStyleSheet('background-color: #ff0000;')

        self.speed_label = QLabel('Скорость: ', self)
        self.speed_label.move(300, 390)
        self.speed_label.setFixedWidth(300)

        self.used_memory_label = QLabel('Используемая память: ', self)
        self.used_memory_label.move(300, 410)
        self.used_memory_label.setFixedWidth(300)

        self.empty_memory_label = QLabel('Свободная память: ', self)
        self.empty_memory_label.move(300, 430)
        self.empty_memory_label.setFixedWidth(300)

        self.system_info_labels = [
            self.speed_label,
            self.used_memory_label,
            self.empty_memory_label
        ]

        # Изначально система не запущена, а значит информацию видеть не должны
        for label in self.system_info_labels:
            label.setVisible(False)

        self.msg_label1 = QLabel('', self)
        self.msg_label1.move(300, 450)
        self.msg_label1.setFixedWidth(300)

        self.msg_label2 = QLabel('', self)
        self.msg_label2.move(300, 470)
        self.msg_label2.setFixedWidth(300)

        self.msg_label3 = QLabel('', self)
        self.msg_label3.move(300, 490)
        self.msg_label3.setFixedWidth(300)

        self.msg_label4 = QLabel('', self)
        self.msg_label4.move(300, 510)
        self.msg_label4.setFixedWidth(300)

        self.msg_label5 = QLabel('', self)
        self.msg_label5.move(300, 530)
        self.msg_label5.setFixedWidth(300)

        self.messages = deque([], 5)

        self.message_labels = [
            self.msg_label1,
            self.msg_label2,
            self.msg_label3,
            self.msg_label4,
            self.msg_label5,
        ]

        # Память
        # Квант
        # Размер команд в тактах
        self.memory_input_label = QLabel('Память системы', self)
        self.memory_input_label.move(50, 350)
        self.memory_input_label.setFixedWidth(100)

        self.memory_input = QLineEdit(self)
        self.memory_input.setValidator(QIntValidator())
        self.memory_input.move(150, 350)
        self.memory_input.setText('1')

        self.kvant_input_label = QLabel('Квант', self)
        self.kvant_input_label.move(50, 400)
        self.kvant_input_label.setFixedWidth(100)

        self.kvant_input = QLineEdit(self)
        self.kvant_input.setValidator(QIntValidator())
        self.kvant_input.move(150, 400)
        self.kvant_input.setText('20')

        self.system_was_started = False

    @pyqtSlot()
    def start_os(self):
        if not system.is_running:
            memory = self.memory_input.text()
            memory = int(memory) if memory else 1

            kvant = self.kvant_input.text()
            kvant = int(kvant) if kvant else 20

            system.memory = from_megabytes_to_bytes(memory)
            system.kvant = kvant

        if not self.system_was_started:
            system.tact_completed.connect(self.redraw_info_label)
            system.start()
            self.system_was_started = True

        system.is_running = True
        self.init_os_button.setDisabled(True)
        self.set_system_params_input_disabled(True)
        self.set_system_button_disabled(False)

        print('Начата работа ОС')

    @pyqtSlot()
    def load_new_task(self):
        """Загрузка новой задачи"""
        loaded = logic.load_new_task()
        if loaded:
            self.messages.append('Задача загружена')
            print('Задача загружена')
        else:
            self.messages.append('Недостаточно памяти для загрузки задачи')
            print('Недостаточно памяти')
        self.redraw_messages_labels()
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
    def redraw_info_label(self):
        self.speed_label.setText(f'Скорость: {system.speed} миллисекунд на тик')
        self.speed_label.setVisible(True)

        used_memory = from_bytes_to_megabytes(system.get_used_memory())
        empty_memory = from_bytes_to_megabytes(system.get_empty_memory())

        self.used_memory_label.setText(f'Используемая память: {used_memory} МБ')
        self.used_memory_label.setVisible(True)

        self.empty_memory_label.setText(f'Свободная память: {empty_memory} МБ')
        self.empty_memory_label.setVisible(True)

    def redraw_messages_labels(self):
        for label in self.message_labels:
            label.setVisible(False)

        for ind, msg in enumerate(self.messages):
            self.message_labels[ind].setText(msg)
            self.message_labels[ind].setVisible(True)

    @pyqtSlot()
    def stop_modeling(self):
        """Остановка моделирования"""
        logic.clean_system()
        for label in self.system_info_labels:
            label.setVisible(False)

        for label in self.message_labels:
            label.setVisible(False)

        self.messages = deque([], 5)
        self.set_system_button_disabled(True)
        self.init_os_button.setDisabled(False)
        self.set_system_params_input_disabled(False)
        print('Система остановлена')

    @pyqtSlot()
    def exit(self):
        sys.exit()

    def set_system_button_disabled(self, value: bool = True):
        """Блокируем или разблокируем кнопки, активные только при запущенной системе"""
        self.load_new_task_button.setDisabled(value)
        self.increase_speed_button.setDisabled(value)
        self.decrease_speed_button.setDisabled(value)
        self.stop_modeling_button.setDisabled(value)

    def set_system_params_input_disabled(self, value: bool = True):
        """Блокируем или разблокируем поля ввода, активные только при выключенной системе"""
        self.memory_input.setDisabled(value)
        self.kvant_input.setDisabled(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OS()
    ex.show()
    sys.exit(app.exec_())
