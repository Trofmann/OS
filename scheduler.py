from typing import List
from typing import Union

from process import Process


class Scheduler(object):
    """Планировщик процессов"""

    def __init__(self):
        self._processes = []  # type: List[Process]

    def append_process(self, process: Process) -> None:
        """Добавление процесса"""
        self._processes.append(process)

    def get_processes(self) -> List[Process]:
        return self._processes

    def _reorder_processes(self):
        """Пересортировка процессов"""
        # TODO: сделать в соответствии с вариантом
        pass

    def get_performing_process(self) -> Union[Process, None]:
        """Получить процесс для исполнения"""
        if self._processes:
            # Пока заглушка в виде первого процесса
            return self._processes[0]
        return None

    def remove_finished_processes(self):
        """Удаление завершённых процессов"""
        old_count = len(self._processes)
        processes = [p for p in self._processes if not p.is_finished]
        self._processes = processes
        if old_count != len(self._processes):
            # Количество изменилось, а значит один из процессов завершился, надо отсортировать
            self._reorder_processes()


scheduler = Scheduler()
