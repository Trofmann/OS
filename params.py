from dataclasses import dataclass


@dataclass
class SystemParams:
    memory: int
    kvant: int
    t_next: int
    t_load: int