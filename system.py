from PyQt5.QtCore import QThread
import time
from cpu import CPU


class System(QThread):
    """Система"""

    def __init__(self):
        super().__init__()
        self.cpu = CPU()
        self.val = 0

    def run(self) -> None:
        while True:
            time.sleep(1)
            self.val += 1


system = System()
