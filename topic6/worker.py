import time

from task_queue import complete_task, fetch_task, reset_task

WORKER_ID = 1


def process_task(task):
    """Эмуляция выполнения задачи."""

    print(
        f'Worker {WORKER_ID} занят задачей {task["id"]}: {task["task_name"]}'
    )

    time.sleep(3)

    print(f'Worker {WORKER_ID} завершил задачу {task["id"]}')


def main():
    """Основной функционал работы Воркера."""

    while True:
        task = fetch_task(WORKER_ID)

        if not task:
            print('Пока задач не обнаружено')
            time.sleep(5)

            continue

        try:
            process_task(task)
            complete_task(task['id'])

        except Exception as err:
            print(
                f'Во время выполнения задачи {task["id"]} произошла ошибка {err}',
            )

            reset_task(task['id'])


if __name__ == '__main__':
    main()
