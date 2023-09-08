from PyQt5.QtCore import QThread
import time
from cpu import CPU
from utils import from_megabytes_to_bytes


class System(QThread):
    """Система"""

    def __init__(self, memory: int, speed: float):
        super().__init__()
        self.cpu = CPU()
        self.memory = memory  # Для удобства в байтах

        self.speed = speed  # миллисекунд на тик
        self.speed_factor = 0.05

    def run(self) -> None:
        """Запуск системы"""
        while True:
            time.sleep(1)

    def increase_speed(self):
        """Увеличение скорости"""
        # Увеличение скорости соответствует уменьшению количества миллисекунд на тик
        self.speed = int((1 - self.speed_factor) * self.speed)

    def decrease_speed(self):
        """Уменьшение скорости"""
        # Уменьшение скорости соответствует увеличению количества миллисекунд на тик
        self.speed = max(int((1 + self.speed_factor) * self.speed), 1)


system = System(
    memory=from_megabytes_to_bytes(75),
    speed=100
)
