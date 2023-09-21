from scheduler import scheduler
import time
from process import Process


class CPU(object):
    """Процессор"""

    def __init__(self, system_):
        self.performing_processes_index = 0  # Индекс исполняемого процесса
        self.system = system_

    def get_used_memory(self) -> int:
        """Получение используемой памяти"""
        # Используемая память процессора есть сумма памяти, занимаемой всем процессами
        processes = scheduler.get_processes()
        return sum([proc.get_used_memory() for proc in processes])

    def _perform_tact(self, process: Process):
        """Выполнение такта"""
        # Выполняем текущий процесс
        process.perform_tact()
        # Выполняем все заблокированные процессы
        blocked_processes = scheduler.get_blocked_processes()
        for blocked_process in blocked_processes:
            blocked_process.perform_tact()
        self.system.send_process_changed_data()

    def perform_frame(self, process: Process) -> int:
        """Выполнение фрейма"""
        duration = 0  # Длительность фрейма
        if process:
            prematurely_finished = False  # Флаг для отправки сигнала, если фрейм завершился преждевременно
            for cur_tact in range(self.system.kvant):
                duration += 1
                if process not in scheduler.get_processes():  # Проверяем, не удалили ли процесс
                    # Удалили, выходим, фрейм завершаем
                    prematurely_finished = True
                    break
                if not process.is_active:
                    # Процесс или завершился, или заблокировался в предыдущем такте
                    prematurely_finished = True
                    break  # Считаем фрейм выполненным преждевременно
                self.system.sleep_for_tacts()
                command = process.current_command
                if command.not_started:
                    # Команда не выполнялась, проверим её полностью
                    tacts_left = self.system.kvant - 1 - cur_tact  # Количество тактов, оставшихся в кванте
                    if command.tacts_left <= tacts_left:  # Команда влезает в квант
                        # Выполним её
                        self._perform_tact(process)
                else:
                    # Команда уже выполнялась, просто продолжим выполнение задачи
                    self._perform_tact(process)
            if prematurely_finished:
                self.system.send_process_changed_data()
        return duration

    @property
    def processes_count(self) -> int:
        """Число загруженных заданий"""
        return scheduler.processes_count
