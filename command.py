import random
from dataclasses import asdict
from typing import List

from params import CommandParams


class Command(object):
    """Команда"""
    TYPE_COMPUTE = 1
    TYPE_INPUT_OUTPUT = 2
    TYPE_STOP = 3

    compute_duration = 4
    io_duration = 40

    # Размер в байтах
    TYPE_SIZE_MAPPING = {
        TYPE_COMPUTE: 2,
        TYPE_INPUT_OUTPUT: 6,
        TYPE_STOP: 0,
    }

    def __init__(self, type_: int):
        self.type_ = type_
        self.tacts_left = self.type_duration_mapping[self.type_]  # Количество тактов до завершения
        self.size = self.TYPE_SIZE_MAPPING[self.type_]

    @property
    def type_duration_mapping(self):
        return {
            self.TYPE_COMPUTE: self.__class__.compute_duration,
            self.TYPE_INPUT_OUTPUT: self.__class__.io_duration,
            self.TYPE_STOP: 0,
        }

    @property
    def is_io(self) -> bool:
        return self.type_ == self.TYPE_INPUT_OUTPUT

    @property
    def not_started(self) -> bool:
        """Команда ещё выполнялась"""
        return self.tacts_left == self.type_duration_mapping[self.type_]

    @classmethod
    def update_params(cls, params: CommandParams):
        """Обновление параметров"""
        params_dict = asdict(params)
        for attr, value in params_dict.items():
            if hasattr(cls, attr):
                setattr(cls, attr, value)
            else:
                raise Exception(f'У команды отсутствует параметр {attr}')


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
