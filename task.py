import random
from command import CommandFabric, Command
from typing import List


class Task(object):
    """Задача"""

    def __init__(self, commands: List[Command]):
        self.commands = commands


class TaskFabric(object):
    @staticmethod
    def generate_random() -> Task:
        # TODO: Проверять свободную память
        commands_count = random.randint(2, 2000)
        commands = CommandFabric.generate_many_random(commands_count - 1)  # Последняя обязательно стоп-команда
        commands.append(CommandFabric.generate_stop())
        return Task(commands)
