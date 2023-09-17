import time
from dataclasses import asdict

from PyQt5.QtCore import QThread, pyqtSignal

from cpu import CPU
from params import SystemParams
from utils import from_megabytes_to_bytes
from scheduler import scheduler


class System(QThread):
    """Система"""
    process_data_changed = pyqtSignal()

    def __init__(self, memory: int, speed: float, kvant: int, t_next: int, t_init_io: int, t_end_io: int, t_load: int):
        super().__init__()
        self.is_running = False

        self.cpu = CPU(system_=self)  # Инициализируем процессор
        self.memory = memory  # Для удобства в байтах

        self.speed = speed  # миллисекунд на такт
        self.speed_factor = 0.05

        self.kvant = kvant  # Квант времени - число тактов моделирования, доступных процессу в состоянии "Активен"
        # (В тактах)

        self.t_next = t_next  # Затраты на выбор процесса для выполнения на процессоре (В тактах)

        self.t_init_io = t_init_io  # Затраты ОС на изменение состояния процесса по обращению ко вводу (выводу)
        # (В тактах)

        self.t_end_io = t_end_io  # Затраты ОС по обслуживанию сигнала окончания (прерывания) ввода (вывода) (В тактах)

        self.t_load = t_load  # Число тактов на загрузку задания

        self.new_tasks_count = 0  # Служебное поле, хранящее количество новых загруженных задач

        self._start_time = time.time()  # Время начала работы

    def run(self) -> None:
        """Запуск системы"""
        while True:
            if self.is_running:
                self.sleep_for_tacts(self.new_tasks_count * self.t_load)
                self.new_tasks_count = 0

                # region Поиск подходящего процесс
                while True:
                    # TODO: на выбор процесса тратится определённое количество тактов
                    # Выбираем первый в очереди процесс, у которого следующая команда не является командой ввода-вывода
                    process = scheduler.get_performing_process()  # Получаем процесс
                    self.send_process_changed_data()
                    if not process:
                        break
                    if process.current_command_is_io:
                        # Заблокируем
                        process.set_blocked()
                        self.send_process_changed_data()
                    else:
                        process.set_active()
                        self.send_process_changed_data()
                        break
                # На выбор процесса потратили такты
                self.sleep_for_tacts(self.t_next)
                # endregion

                self.cpu.perform_frame(process)
                if process in scheduler.get_processes() and process.is_active:
                    process.set_ready()
                    self.send_process_changed_data()

                self.sleep_for_tacts()
                blocked_processes = scheduler.get_blocked_processes()
                for blocked_process in blocked_processes:
                    blocked_process.perform_tact()
                self.send_process_changed_data()

    def sleep_for_tacts(self, count_: int = 1) -> None:
        time.sleep((self.speed * count_) / 1000)

    def send_process_changed_data(self) -> None:
        """Отправка сигнала"""
        self.process_data_changed.emit()

    def increase_speed(self) -> None:
        """Увеличение скорости"""
        # Увеличение скорости соответствует уменьшению количества миллисекунд на тик
        self.speed = max(int((1 - self.speed_factor) * self.speed), 1)

    def decrease_speed(self) -> None:
        """Уменьшение скорости"""
        # Уменьшение скорости соответствует увеличению количества миллисекунд на тик
        self.speed = max(int((1 + self.speed_factor) * self.speed), 1)

    def get_used_memory(self) -> int:
        """Используемая память"""
        return self.cpu.get_used_memory()

    def get_empty_memory(self) -> int:
        """Получение свободной памяти"""
        used_memory = self.get_used_memory()
        return self.memory - used_memory

    @property
    def process_count(self) -> int:
        """Число загруженных заданий"""
        return self.cpu.processes_count

    @property
    def working_time(self) -> float:
        """Время работы"""
        return time.time() - self._start_time

    def update_params(self, params: SystemParams) -> None:
        """Обновление параметров"""
        params_dict = asdict(params)
        for attr, value in params_dict.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
            else:
                raise Exception('У системы отсутствует такой параметр')



system = System(
    memory=from_megabytes_to_bytes(1),
    # memory=10000, # Для отладки невозможности загрузки задачи
    speed=100,
    kvant=20,
    t_next=4,
    t_init_io=0,
    t_end_io=0,
    t_load=1
)
