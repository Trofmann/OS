import time

from PyQt5.QtCore import QThread, pyqtSignal

from cpu import CPU
from utils import from_megabytes_to_bytes


class System(QThread):
    """Система"""
    tact_completed = pyqtSignal()

    def __init__(self, memory: int, speed: float, kvant: int, t_next: int, t_init_io: int, t_end_io: int, t_load: int):
        super().__init__()
        self.is_running = False

        self.cpu = CPU()  # Инициализируем процессор
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

        self._start_time = time.time()  # Время начала работы
        self._completed_tasks_count = 0  # Число выполненных задач

    def run(self) -> None:
        """Запуск системы"""
        while True:
            time.sleep(self.speed / 1000)  # Такт
            completed = self.cpu.perform_tact()
            self._completed_tasks_count += completed
            # print(self.get_empty_memory()) # Для отладки
            self.tact_completed.emit()  # Отправляем

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

    @property
    def completed_tasks_count(self) -> int:
        """Число выполненных задач"""
        return self._completed_tasks_count


system = System(
    memory=from_megabytes_to_bytes(75),
    # memory=75, # Для отладки невозможности загрузки задачи
    speed=100,
    kvant=0,
    t_next=0,
    t_init_io=0,
    t_end_io=0,
    t_load=0
)
