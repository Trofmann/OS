from typing import List, Union

from process import Process


class Scheduler(object):
    """Планировщик процессов"""

    def __init__(self):
        self._processes = []  # type: List[Process]
        self.completed_tasks_count = 0  # Число выполненных задач

    def append_process(self, process: Process) -> None:
        """Добавление процесса"""
        self._processes.append(process)

    def get_processes(self) -> List[Process]:
        return self._processes

    def clean_processes(self) -> None:
        """Очистка списка процессов"""
        self._processes = []

    def _reorder_processes(self):
        """Пересортировка процессов"""
        self._processes.sort(key=lambda p: p.priority, reverse=True)

    def filter_processes(self, states: List[int]) -> List[Process]:
        """Фильтрация процессов по состоянию"""
        return list(filter(lambda p: p.state in states, self._processes))

    def get_ready_processes(self) -> List[Process]:
        """Процессы в состоянии 'Готов'"""
        return self.filter_processes([Process.STATE_READY])

    def get_blocked_processes(self) -> List[Process]:
        """Процессы в состоянии 'Заблокирован'"""
        return self.filter_processes([Process.STATE_BLOCKED])

    def get_performing_process(self) -> Union[Process, None]:
        """Получить процесс для исполнения"""
        self._reorder_processes()
        ready_processes = self.get_ready_processes()
        if ready_processes:
            # Первый готовый процесс
            return ready_processes[0]
        return None

    def remove_finished_processes(self) -> bool:
        """Удаление завершённых процессов"""
        pass
        # completed = False  # Задача завершена
        # old_count = len(self._processes)
        # processes = [p for p in self._processes if not p.is_finished]
        # self._processes = processes
        # if old_count != len(self._processes):
        #     # Количество изменилось, а значит один из процессов завершился, надо отсортировать
        #     self._reorder_processes()
        #     completed = True
        # return completed

    @property
    def processes_count(self) -> int:
        """Число загруженных заданий"""
        return len(self._processes)

    def remove_process(self, uid: str) -> bool:
        """Удаление процесса по uid"""
        error = True
        found = list(filter(lambda p: p.uid == uid, self._processes))
        if found:
            self._processes.remove(found[0])
            error = False
        return error


scheduler = Scheduler()
