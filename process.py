import random
from uuid import uuid4
from task import Task, TaskFabric


class Process(object):
    """Процесс"""
    STATE_ACTIVE = 1
    STATE_READY = 2
    STATE_BLOCKED = 3
    STATE_FINISHED = 4

    STATE_VERBOSE = {
        1: 'Активный',
        2: 'Готов',
        3: 'Заблокирован',
        4: 'Завершён',
    }

    def __init__(self, task: Task, state: int = STATE_READY):
        self.task = task
        self.task.process = self
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

    @property
    def is_finished(self) -> bool:
        return self.check_state(self.STATE_FINISHED)

    def _set_state(self, state: int) -> None:
        self.state = state

    def set_active(self) -> None:
        self._set_state(self.STATE_ACTIVE)

    def set_ready(self) -> None:
        self._set_state(self.STATE_READY)

    def set_blocked(self) -> None:
        self._set_state(self.STATE_BLOCKED)

    def set_finished(self) -> None:
        self._set_state(self.STATE_FINISHED)

    def get_state_display(self):
        return self.STATE_VERBOSE[self.state]

    def perform_tact(self) -> None:
        """Выполнение такта"""
        command_finished = self.task.perform_tact()
        if command_finished:
            try:
                current_command = self.current_command
                if current_command.is_io:
                    # Новая команда является командой ввода-вывода, заблокируем процесс
                    self.set_blocked()
                else:
                    # Новая команда не является командой ввода-вывода, процесс готов к выполнению
                    self.set_ready()
            except IndexError:  # Вышли за пределы списка команд, значит задача выполнена
                self.set_finished()

    def get_commands(self):
        return self.task.commands

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
        """Время нахождения в списке готовности (Простой процесса) в процентах от времени выполнения задания"""
        return 0

    @property
    def current_command_is_io(self) -> bool:
        """Следующая команда является командой ввода вывода"""
        return self.task.current_command_is_io

    @property
    def current_command(self):
        return self.task.current_command


class ProcessFabric(object):
    @staticmethod
    def generate_random() -> Process:
        task_ = TaskFabric.generate_random()
        return Process(task_)
