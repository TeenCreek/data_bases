import datetime
import time

from decorators import single


@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction():
    print('Начинается обработка транзакции')
    time.sleep(2)
    print('Транзакция обработана')


if __name__ == '__main__':
    process_transaction()
