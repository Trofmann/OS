import random
from typing import List


class Command(object):
    """Команда"""
    TYPE_COMPUTE = 1
    TYPE_INPUT_OUTPUT = 2
    TYPE_STOP = 3

    # Продолжительность в тактах
    TYPE_DURATION_MAPPING = {
        TYPE_COMPUTE: 4,
        TYPE_INPUT_OUTPUT: 40,
        TYPE_STOP: 0,
    }

    # Размер в байтах
    TYPE_SIZE_MAPPING = {
        TYPE_COMPUTE: 2,
        TYPE_INPUT_OUTPUT: 6,
        TYPE_STOP: 0,
    }

    def __init__(self, type_: int):
        self.type_ = type_
        self.tacts_left = self.TYPE_DURATION_MAPPING[self.type_]  # Количество тактов до завершения
        self.size = self.TYPE_SIZE_MAPPING[self.type_]


class CommandFabric(object):
    @staticmethod
    def generate_random() -> Command:
        type_ = random.choice([Command.TYPE_COMPUTE, Command.TYPE_INPUT_OUTPUT])  # Стоп-команда будет последней
        return Command(type_=type_)

    @staticmethod
    def generate_compute() -> Command:
        return Command(type_=Command.TYPE_COMPUTE)

    @staticmethod
    def generate_input_output() -> Command:
        return Command(type_=Command.TYPE_INPUT_OUTPUT)

    @staticmethod
    def generate_stop() -> Command:
        return Command(type_=Command.TYPE_STOP)

    @classmethod
    def generate_many_random(cls, count: int) -> List[Command]:
        return [cls.generate_random() for _ in range(count)]
