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

    # def perform_tact(self, process: Process) -> bool:
    #     """Выполнение такта"""
    # completed = False  # Процесс завершён
    # process = scheduler.get_performing_process()
    # if process:
    #     process.perform_tact()
    #     completed = scheduler.remove_finished_processes()
    # return completed

    def perform_frame(self):
        """Выполнение фрейма"""
        while True:
            # TODO: на выбор процесса тратится определённое количество тактов
            # Выбираем первый в очереди процесс, у которого следующая команда не является командой ввода-вывода
            process = scheduler.get_performing_process()  # Получаем процесс
            if not process:
                break
            if process.current_command_is_io:
                # Заблокируем
                process.set_blocked()
            else:
                process.set_active()
                break
        prematurely_finished = False  # Флаг для отправки сигнала, если фрейм завершился преждевременно
        for cur_tact in range(self.system.kvant):
            if process not in scheduler.get_processes():  # Проверяем, не удалили ли процесс
                # Удалили, выходим, фрейм завершаем
                prematurely_finished = True
                break
            if not process.is_active:
                # Процесс или завершился в предыдущем такте
                prematurely_finished = True
                break  # Считаем фрейм выполненным преждевременно
            time.sleep(self.system.speed / 1000)  # Такт
            command = process.current_command
            if command.not_started:
                # Команда не выполнялась, проверим её полностью
                tacts_left = self.system.kvant - 1 - cur_tact  # Количество тактов, оставшихся в кванте
                if command.is_io:
                    # В процессе выполнения кванта встретили команду ввода вывода
                    process.set_blocked()  # заблокируем процесс
                    prematurely_finished = True
                    break  # завершим фрейм
                if command.tacts_left <= tacts_left:  # Команда влезает в квант
                    # Выполним её
                    process.perform_tact()
            else:
                # Команда выполнялась, просто продолжим выполнение задачи
                process.perform_tact()
            self.system.tact_completed.emit()

        if prematurely_finished:
            self.system.tact_completed.emit()

    @property
    def processes_count(self) -> int:
        """Число загруженных заданий"""
        return scheduler.processes_count
