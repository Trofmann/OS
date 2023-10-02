from process import ProcessFabric
from scheduler import scheduler
from system import system


def load_new_task() -> bool:
    """Загрузка новой задачи"""
    # Загрузка новой задачи есть создание процесса с этой задачей и добавление процесс в планировщик
    process_ = ProcessFabric.generate_random(system.tacts_count)
    if system.get_empty_memory() >= process_.get_used_memory():
        scheduler.append_process(process_)
        system.new_tasks_count += 1
        return True
    return False


def clean_system() -> None:
    system.is_running = False
    system.cpu.performing_processes_index = 0  # Сброс счётчика
    system.new_tasks_count = 0
    system.tacts_count = 0
    system.system_tacks_count = 0
    system.completed_tasks_count = 0
    scheduler.clean_processes()
    scheduler.completed_tasks_count = 0  # Сбрасываем счётчик
