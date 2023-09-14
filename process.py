import random
from uuid import uuid4
from task import Task, TaskFabric


class Process(object):
    """Процесс"""
    STATE_ACTIVE = 1
    STATE_READY = 2
    STATE_BLOCKED = 3

    STATE_VERBOSE = {
        1: 'Активный',
        2: 'Готов',
        3: 'Заблокирован',
    }

    def __init__(self, task: Task, state: int = STATE_READY):
        self.task = task
        self.state = state
        self.uid = str(uuid4())

    def check_state(self, state: int) -> bool:
        return self.state == state

    def get_used_memory(self) -> int:
        """Получение используемой памяти"""
        # Используемая память процесса есть сумма занимаемой памяти всех команд
        return sum([comm.size for comm in self.task.commands])

    @property
    def is_active(self) -> bool:
        return self.check_state(self.STATE_ACTIVE)

    @property
    def is_ready(self) -> bool:
        return self.check_state(self.STATE_READY)

    @property
    def is_blocked(self) -> bool:
        return self.check_state(self.STATE_BLOCKED)

    def get_state_display(self):
        return self.STATE_VERBOSE[self.state]

    def perform_tact(self) -> None:
        """Выполнение такта"""
        self.task.perform_tact()

    @property
    def is_finished(self) -> bool:
        """Признак завершения процесса"""
        return self.task.is_finished

    @property
    def priority(self) -> int:
        """Приоритет процессора"""
        return self.task.priority

    @property
    def current_command_index(self) -> int:
        """Индекс текущей исполняемой команды"""
        return self.task.current_command_index

    @property
    def ready_time(self) -> int:
        """Время нахождения в списке готовности (Простой процесс) в процентах от времени выполнения задания"""
        return 0


class ProcessFabric(object):
    @staticmethod
    def generate_random() -> Process:
        task_ = TaskFabric.generate_random()
        return Process(task_)
