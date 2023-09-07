from process import ProcessFabric
from scheduler import scheduler


def load_new_task():
    """Загрузка новой задачи"""
    # Загрузка новой задачи есть создание процесса с этой задачей и добавление процесс в планировщик
    process_ = ProcessFabric.generate_random()
    scheduler.append_process(process_)
