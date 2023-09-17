from dataclasses import dataclass


@dataclass
class SystemParams:
    memory: int
    kvant: int
    t_next: int
    t_load: int


@dataclass
class CommandParams:
    compute_duration: int
    io_duration: int
