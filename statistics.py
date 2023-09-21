from dataclasses import dataclass
from typing import List

from system import system


@dataclass
class ProcessStartStopData:
    start: int  # Такт, на котором процесс загрузили
    stop: int  # Такт, на котором процесс вывели из системы

    @property
    def duration(self) -> int:
        return self.stop - self.start


class SystemStatisticsProxy(object):
    """Статистические данные системы"""

    def __init__(self):
        # self.system = system
        self._process_data = list()  # type:List[ProcessStartStopData]

    def _get_loaded_tasks_count(self) -> int:
        """Число загруженных задач"""
        from scheduler import scheduler
        return len(scheduler.get_processes())

    def _get_system_costs(self) -> str:
        """Системные затраты в процентах"""
        value = 0
        if system.tacks_count:
            value = round((system.system_tacks_count / system.tacks_count) * 100, 0)
        return f'{value} %'

    def _get_working_time(self) -> int:
        """Время работы системы в тактах"""
        return system.tacts_count

    def _get_completed_tasks_count(self) -> int:
        """Число выполненных задач"""
        return system.completed_tasks_count

    def _get_turnaround_time(self) -> float:
        """Оборотное время"""
        # Находится как среднестатистическое время, прошедшее с момента загрузки процесса в систему,
        # до его вывода из системы в связи с завершением
        durations = [data.duration for data in self._process_data]
        return round(sum(durations) / len(durations), 2)

    def add_process_data(self, start: int, stop: int) -> None:
        self._process_data.append(ProcessStartStopData(start, stop))

    def dump(self) -> str:
        info_funcs = [
            self._get_loaded_tasks_count,
            self._get_completed_tasks_count,
            self._get_working_time,
            self._get_system_costs,
            self._get_turnaround_time,
        ]
        info = []
        for func in info_funcs:
            name = func.__doc__
            value = func.__call__()
            info.append(f'{name}: {value}')
        return '\n'.join(info)


statistics = SystemStatisticsProxy()
