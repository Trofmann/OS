import random

from task import Task, TaskFabric


class Process(object):
    """Процесс"""
    STATE_ACTIVE = 1
    STATE_READY = 2
    STATE_BLOCKED = 3

    def __init__(self, task: Task, priority: int, state: int = STATE_READY):
        self.task = task
        self.state = state
        self.priority = priority

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


class ProcessFabric(object):
    @staticmethod
    def generate_random() -> Process:
        task_ = TaskFabric.generate_random()
        priority = random.randint(1, 100)
        return Process(task_, priority=priority)
