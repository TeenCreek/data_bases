import random
import time
from dataclasses import dataclass

import redis


class RateLimitExceed(Exception):
    pass


@dataclass
class RateLimiterConfig:
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    max_requests: int = 5
    window_seconds: int = 3
    key: str = 'api_requests'


class RateLimiter:
    def __init__(self, config):
        self.config = config
        self.redis = redis.StrictRedis(
            host=config.redis_host,
            port=config.redis_port,
            db=config.redis_db,
        )

        self.max_requests = config.max_requests
        self.window_seconds = config.window_seconds
        self.key = config.key

    def test(self):
        current_time = time.time()

        self.redis.zadd(self.key, {current_time: current_time})
        self.redis.expire(self.key, self.window_seconds)

        self.redis.zremrangebyscore(
            self.key, '-inf', current_time - self.window_seconds
        )

        return self.redis.zcard(self.key) <= self.max_requests


def make_api_request(rate_limiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # Какая-то бизнес-логика
        pass


if __name__ == '__main__':
    config = RateLimiterConfig()
    rate_limiter = RateLimiter(config)

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print('Превышен лимит запросов')
        else:
            print('Все в порядке')
