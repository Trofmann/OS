from scheduler import scheduler


class CPU(object):
    """Процессор"""

    def __init__(self):
        pass

    def get_used_memory(self) -> int:
        """Получение используемой памяти"""
        # Используемая память процессора есть сумма памяти, занимаемой всем процессами
        processes = scheduler.get_processes()
        return sum([proc.get_used_memory() for proc in processes])
