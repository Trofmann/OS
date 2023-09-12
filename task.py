import random
from command import CommandFabric, Command
from typing import List


class Task(object):
    """Задача"""

    def __init__(self, commands: List[Command]):
        self.commands = commands
        self.current_command_index = 0

    def perform_tact(self):
        """Выполнение такта"""
        self.commands[self.current_command_index].tacts_left -= 1
        # Команда завершила своё исполнение, переместим указатель
        print(self.current_command_index, len(self.commands))
        if self.commands[self.current_command_index].tacts_left <= 0:  # Для стоп-команды
            self.current_command_index += 1

    @property
    def is_finished(self):
        """Признак завершения задачи"""
        # Задача завершена, если дошли до конца
        return self.current_command_index == len(self.commands)


class TaskFabric(object):
    @staticmethod
    def generate_random() -> Task:
        commands_count = random.randint(2, 2000)
        commands = CommandFabric.generate_many_random(commands_count - 1)  # Последняя обязательно стоп-команда
        commands.append(CommandFabric.generate_stop())
        return Task(commands)
