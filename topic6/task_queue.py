from db import get_connection, release_connection


def execute_query(query, params=None, fetch=False):
    """Универсальная функция для выполнения запросов к БД."""

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(query, params)

            if fetch:
                return cur.fetchone()

            conn.commit()

    except Exception as err:
        conn.rollback()

        raise err

    finally:
        release_connection(conn)


def fetch_task(worker_id):
    """Берет задачу со статусом pending для выполнения."""

    query_select = """
        SELECT id, task_name
        FROM tasks
        WHERE status = 'pending'
        FOR UPDATE SKIP LOCKED
        LIMIT 1;
    """

    query_update = """
        UPDATE tasks
        SET status = 'processing', worker_id = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
    """

    task = execute_query(query_select, fetch=True)

    if not task:
        return None

    execute_query(query_update, (worker_id, task['id']))

    return task


def complete_task(task_id):
    """Обновление статуса задачи на completed."""

    query = """
        UPDATE tasks
        SET status = 'completed', updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
    """

    execute_query(query, (task_id,))


def reset_task(task_id):
    """Сброс статуса задачи на pending при возникновении ошибки."""

    query = """
        UPDATE tasks
        SET status = 'pending', worker_id = NULL, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
    """

    execute_query(query, (task_id,))
