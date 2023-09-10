import random
from command import CommandFabric, Command
from typing import List


class Task(object):
    """Задача"""

    def __init__(self, commands: List[Command]):
        self.commands = commands

    def perform_tact(self):
        """Выполнение такта"""
        self.commands[0].tacts_left -= 1
        # Команда завершила своё исполнение, удалим её из задачи
        if self.commands[0].tacts_left == 0:
            self.commands.pop(0)

    @property
    def is_finished(self):
        """Признак завершения задачи"""
        # Задача завершена, если нет команд для выполнения
        return not bool(self.commands)


class TaskFabric(object):
    @staticmethod
    def generate_random() -> Task:
        commands_count = random.randint(2, 2000)
        commands = CommandFabric.generate_many_random(commands_count - 1)  # Последняя обязательно стоп-команда
        commands.append(CommandFabric.generate_stop())
        return Task(commands)
