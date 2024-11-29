import json
import os
from dataclasses import asdict, dataclass

import redis
from dotenv import load_dotenv

load_dotenv()


rds = redis.StrictRedis(
    host=os.getenv('REDIS_HOST', default='localhost'),
    port=os.getenv('REDIS_PORT', default=6379),
    db=os.getenv('REDIS_DB', default=0),
    decode_responses=True,
)


@dataclass
class Message:
    key: str
    value: int


class RedisQueue:
    def __init__(self, queue_name='queue'):
        self.queue_name = queue_name

    def publish(self, msg):
        """Публикация сообщеня в очередь."""

        try:
            rds.rpush(self.queue_name, json.dumps(asdict(msg)))

        except redis.RedisError as err:
            print(f'Ошибка при публикации сообщения в очередь: {err}')

    def consume(self):
        """Извлечение и возврат первого сообщения из очереди."""

        try:
            msg = rds.lpop(self.queue_name)

            if msg:
                msg_dict = json.loads(msg)

                return Message(**msg_dict)

        except redis.RedisError as err:
            print(f'Ошибка при получении сообщения из очереди: {err}')

        return None


if __name__ == '__main__':
    q = RedisQueue()

    q.publish(Message(key='a', value=1))
    q.publish(Message(key='b', value=2))
    q.publish(Message(key='c', value=3))

    assert q.consume() == Message(key='a', value=1)
    assert q.consume() == Message(key='b', value=2)
    assert q.consume() == Message(key='c', value=3)

    print('Все тесты прошли успешно')
