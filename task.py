import random
from command import CommandFabric, Command
from typing import List
from uuid import uuid4


class Task(object):
    """Задача"""

    def __init__(self, commands: List[Command], priority: int, process_=None):
        self.commands = commands
        self.current_command_index = 0
        self.priority = priority  # Приоритет задания
        self.uid = str(uuid4())  # Генерируем в момент создания задачи
        self.process = process_  # Процесс, которому принадлежит задача

    def perform_tact(self) -> bool:
        """Выполнение такта"""
        command_finished = False  # Команда завершила выполнение
        self.commands[self.current_command_index].tacts_left -= 1
        # print(self.current_command_index, len(self.commands), self.current_command.type_)
        # Команда завершила своё исполнение, переместим указатель
        if self.commands[self.current_command_index].tacts_left <= 0:  # Для стоп-команды
            self.current_command_index += 1
            command_finished = True
        return command_finished

    @property
    def current_command_is_io(self) -> bool:
        """Следующая задача является командой ввода вывода"""
        return self.commands[self.current_command_index].is_io

    @property
    def current_command(self) -> Command:
        return self.commands[self.current_command_index]

    @property
    def commands_count(self) -> int:
        return len(self.commands)


class TaskFabric(object):
    @staticmethod
    def generate_random() -> Task:
        commands_count = random.randint(2, 2000)
        commands = CommandFabric.generate_many_random(commands_count - 1)  # Последняя обязательно стоп-команда
        commands.append(CommandFabric.generate_stop())
        priority = random.randint(1, 100)
        return Task(commands, priority)
