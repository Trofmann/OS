from task import Task


class Process(object):
    """Процесс"""
    STATE_ACTIVE = 1
    STATE_READY = 2
    STATE_BLOCKED = 3

    def __init__(self, task: Task, state: int = STATE_READY):
        self.task = task
        self.state = state

    def check_state(self, state: int) -> bool:
        return self.state == state

    @property
    def is_active(self) -> bool:
        return self.check_state(self.STATE_ACTIVE)

    @property
    def is_ready(self) -> bool:
        return self.check_state(self.STATE_READY)

    @property
    def is_blocked(self) -> bool:
        return self.check_state(self.STATE_BLOCKED)
