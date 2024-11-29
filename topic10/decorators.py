import time
from functools import wraps

from redis_conf import redis_connection


def try_lock(rds, lock_key, max_processing_time, retry_time, max_retries):
    for retries in range(max_retries):
        if rds.setnx(lock_key, 'locked'):
            rds.expire(lock_key, max_processing_time)
            return True
        print(
            f'Функция уже выполняется. Попытка №{retries + 1} для получения блокировки.'
        )
        time.sleep(retry_time)

    return False


def single(max_processing_time, retry_time=1, max_retries=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            rds = redis_connection()
            lock_key = f'lock:{func.__name__}'

            if try_lock(
                rds, lock_key, max_processing_time, retry_time, max_retries
            ):
                try:
                    print(f'Блокировка получена для функции {func.__name__}')
                    return func(*args, **kwargs)
                finally:
                    rds.delete(lock_key)
                    print(
                        f'Блокировка освобождена для функции {func.__name__}'
                    )
            else:
                print(
                    f'Не удалось получить блокировку для функции {func.__name__} после {max_retries} попыток.'
                )

            return None

        return wrapper

    return decorator
