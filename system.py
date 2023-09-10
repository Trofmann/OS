import time

from PyQt5.QtCore import QThread, pyqtSignal

from cpu import CPU
from utils import from_megabytes_to_bytes


class System(QThread):
    """Система"""
    tact_completed = pyqtSignal()

    def __init__(self, memory: int, speed: float):
        super().__init__()
        self.is_running = False

        self.cpu = CPU()  # Инициализируем процессор
        self.memory = memory  # Для удобства в байтах

        self.speed = speed  # миллисекунд на такт
        self.speed_factor = 0.05

    def run(self) -> None:
        """Запуск системы"""
        while True:
            time.sleep(self.speed / 1000)  # Такт
            self.cpu.perform_tact()
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


system = System(
    memory=from_megabytes_to_bytes(75),
    # memory=75, # Для отладки невозможности загрузки задачи
    speed=100
)
