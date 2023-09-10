from process import ProcessFabric
from scheduler import scheduler
from system import system


def load_new_task() -> bool:
    """Загрузка новой задачи"""
    # Загрузка новой задачи есть создание процесса с этой задачей и добавление процесс в планировщик
    # TODO: Проверять свободную память
    process_ = ProcessFabric.generate_random()
    if system.get_empty_memory() >= process_.get_used_memory():
        scheduler.append_process(process_)
        return True
    return False
