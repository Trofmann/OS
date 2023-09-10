from scheduler import scheduler


class CPU(object):
    """Процессор"""

    def __init__(self):
        self.performing_processes_index = 0  # Индекс исполняемого процесса

    def get_used_memory(self) -> int:
        """Получение используемой памяти"""
        # Используемая память процессора есть сумма памяти, занимаемой всем процессами
        processes = scheduler.get_processes()
        return sum([proc.get_used_memory() for proc in processes])

    def perform_tact(self):
        """Выполнение такта"""
        process = scheduler.get_performing_process()
        if process:
            process.perform_tact()
            scheduler.remove_finished_processes()
