from typing import List
from process import Process


class Scheduler(object):
    """Планировщик процессов"""

    def __init__(self):
        self._processes = []  # type: List[Process]

    def append_process(self, process: Process) -> None:
        """Добавление процесса"""
        self._processes.append(process)

    def reorder_processes(self):
        """Пересортировка процессов"""
        # TODO: сделать в соответствии с вариантом
        return self._processes
