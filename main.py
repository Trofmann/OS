import sys
from collections import deque

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *

import logic
from command import Command
from forms import SystemParamsForm, CommandParamsForm
from params import SystemParams, CommandParams
from process import Process
from scheduler import scheduler
from system import system
from statistics import statistics
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
        self.resize(1700, 900)  # размер окна

        # region Кнопки
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

        self.remove_process_button = QPushButton('Удалить процесс', self)
        self.remove_process_button.move(50, 220)
        self.remove_process_button.setFixedWidth(200)
        self.remove_process_button.setToolTip('Удалить процесс')
        self.remove_process_button.clicked.connect(self.remove_process)

        self.stop_modeling_button = QPushButton('Завершить моделирование', self)
        self.stop_modeling_button.move(50, 250)
        self.stop_modeling_button.setFixedWidth(200)
        self.stop_modeling_button.setToolTip('Завершить моделирование')
        self.stop_modeling_button.clicked.connect(self.stop_modeling)

        self.set_system_button_disabled(True)

        self.exit_button = QPushButton('Выйти', self)
        self.exit_button.move(50, 280)
        self.exit_button.setFixedWidth(200)
        self.exit_button.setToolTip('Выйти')
        self.exit_button.clicked.connect(self.exit)
        self.exit_button.setStyleSheet('background-color: #ff0000;')
        # endregion

        # region Информация
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
        # endregion

        # region Сообщения
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
        # endregion

        # region Ввод параметров системы
        self.system_params_label = QLabel('Параметры системы', self)
        self.system_params_label.move(50, 315)
        self.system_params_label.setFixedWidth(200)

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

        self.t_next_input_label = QLabel('Выбор процесса', self)
        self.t_next_input_label.move(50, 450)
        self.t_next_input_label.setFixedWidth(100)

        self.t_next_input = QLineEdit(self)
        self.t_next_input.setValidator(QIntValidator())
        self.t_next_input.move(150, 450)
        self.t_next_input.setText('4')

        self.t_load_input_label = QLabel('Загрузка задачи', self)
        self.t_load_input_label.move(50, 500)
        self.t_load_input_label.setFixedWidth(100)

        self.t_load_input = QLineEdit(self)
        self.t_load_input.setValidator(QIntValidator())
        self.t_load_input.move(150, 500)
        self.t_load_input.setText('1')

        self.system_params_inputs = [
            self.memory_input, self.kvant_input, self.t_next_input, self.t_load_input
        ]

        # endregion

        # region Ввод параметров команд
        self.commands_params_label = QLabel('Продолжительность команд', self)
        self.commands_params_label.move(50, 580)
        self.commands_params_label.setFixedWidth(200)

        self.compute_command_input_label = QLabel('Вычислительная', self)
        self.compute_command_input_label.move(50, 620)
        self.compute_command_input_label.setFixedWidth(100)

        self.compute_command_input = QLineEdit(self)
        self.compute_command_input.setValidator(QIntValidator())
        self.compute_command_input.move(150, 620)
        self.compute_command_input.setText('4')

        self.io_command_input_label = QLabel('Ввод/вывод', self)
        self.io_command_input_label.move(50, 670)
        self.io_command_input_label.setFixedWidth(100)

        self.io_command_input = QLineEdit(self)
        self.io_command_input.setValidator(QIntValidator())
        self.io_command_input.move(150, 670)
        self.io_command_input.setText('40')

        self.command_params_inputs = [
            self.compute_command_input, self.io_command_input
        ]
        # endregion

        self.params_inputs = self.system_params_inputs + self.command_params_inputs

        # region Таблица процессов
        self.processes_table = QTableWidget(self)
        self.processes_table.setColumnCount(6)
        self.processes_table.setRowCount(0)
        self.processes_table.move(300, 100)
        self.processes_table.setFixedWidth(1200)
        self.processes_table.setFixedHeight(200)
        self.processes_table.setHorizontalHeaderLabels([
            'uid', 'Статус', 'Объём памяти', 'Счётчик команд', 'Всего команд', 'Приоритет'
        ])

        for i in range(6):
            self.processes_table.setColumnWidth(i, 200)

        # endregion

        # region Статистика
        self.statistic = QLabel(statistics.dump(), self)
        self.statistic.move(800, 400)
        self.statistic.setFixedHeight(200)
        self.statistic.setFixedWidth(500)
        system.statistics_changed.connect(self.redraw_statistic)
        # endregion

        self.system_was_started = False

    # region Обработка нажатий кнопок
    @pyqtSlot()
    def start_os(self):
        if not system.is_running:
            system_params = self.extract_system_params()
            system.update_params(system_params)

            command_params = self.extract_command_params()
            Command.update_params(command_params)

        if not self.system_was_started:
            self.redraw_speed_label()
            self.redraw_after_tact()
            system.process_data_changed.connect(self.redraw_after_tact)
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
        self.redraw_processes_table()
        print(f'Свободная память {system.get_empty_memory()} байт')

    @pyqtSlot()
    def increase_speed(self):
        system.increase_speed()
        self.redraw_speed_label()
        print(f'{system.speed} миллисекунд на тик')

    @pyqtSlot()
    def decrease_speed(self):
        system.decrease_speed()
        self.redraw_speed_label()
        print(f'{system.speed} миллисекунд на тик')

    @pyqtSlot()
    def redraw_after_tact(self):
        """Перерисовка объектов, которые меняются каждый такт"""
        self.redraw_info_label()
        self.redraw_processes_table()

    @pyqtSlot()
    def remove_process(self):
        """Удаление процесса"""
        process_uid, ok = QInputDialog.getText(
            self, 'Удаление процесс', 'Введите uid процесса',
        )
        if ok:
            error = scheduler.remove_process(process_uid)
            if error:
                self.messages.append('Не удалось удалить процесс')
            else:
                self.messages.append('Процесс удалён')
            self.redraw_messages_labels()
        self.redraw_processes_table()

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

    # endregion

    # region Отрисовка
    def redraw_speed_label(self):
        self.speed_label.setText(f'Скорость: {system.speed} миллисекунд на тик')
        self.speed_label.setVisible(True)

    def redraw_info_label(self):
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

    def redraw_processes_table(self):
        """Перерисовка таблицы процессов"""
        processes = scheduler.get_processes()
        self.processes_table.setRowCount(len(processes))
        for row, process in enumerate(processes):  # type: int, Process
            row_data = [
                process.uid,
                process.get_state_display(),
                str(process.get_used_memory()),
                str(process.task.current_command_index),
                str(process.commands_count),
                str(process.priority),
            ]
            for col, value in enumerate(row_data):
                self.processes_table.setItem(row, col, QTableWidgetItem(value))

    def redraw_statistic(self):
        """Перерисовка статистики"""
        self.statistic.setText(statistics.dump())

    # endregion

    # region Установка доступности
    def set_system_button_disabled(self, value: bool = True):
        """Блокируем или разблокируем кнопки, активные только при запущенной системе"""
        self.load_new_task_button.setDisabled(value)
        self.increase_speed_button.setDisabled(value)
        self.decrease_speed_button.setDisabled(value)
        self.stop_modeling_button.setDisabled(value)
        self.remove_process_button.setDisabled(value)

    def set_system_params_input_disabled(self, value: bool = True):
        """Блокируем или разблокируем поля ввода, активные только при выключенной системе"""
        for input_ in self.params_inputs:
            input_.setDisabled(value)

    # endregion

    # region Извлечение данных из полей
    def extract_system_params(self) -> SystemParams:
        """Извлечение параметров системы из полей ввода"""
        form = SystemParamsForm(self)
        params = form.clean()
        return params

    def extract_command_params(self) -> CommandParams:
        """Извлечение параметров команд из полей ввода"""
        form = CommandParamsForm(self)
        params = form.clean()
        return params
    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OS()
    ex.show()
    sys.exit(app.exec_())
