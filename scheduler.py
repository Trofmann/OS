from typing import List
from process import Process, ProcessFabric


class Scheduler(object):
    """Планировщик процессов"""

    def __init__(self):
        self._processes = []  # type: List[Process]

    def append_process(self, process: Process) -> None:
        """Добавление процесса"""
        self._processes.append(process)
        self.reorder_processes()

    def get_processes(self) -> List[Process]:
        return self._processes

    def reorder_processes(self):
        """Пересортировка процессов"""
        # TODO: сделать в соответствии с вариантом
        pass

    def get_performing_process(self):
        """Получить процесс для исполнения"""
        # TODO: придумать, в какой момент удалять завершившиеся процессы
        if self._processes:
            # Пока заглушка в виде первого процесса
            return self._processes[0]
        return None


scheduler = Scheduler()
