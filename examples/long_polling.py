import os
import time
import requests
from dotenv import load_dotenv


load_dotenv()


API_URL = 'https://api.telegram.org/bot'
TOKEN = os.getenv('BOT_TOKEN')
TEXT = 'long pooling'


def do_something() -> None:
    print('произошел апдейт')
    time.sleep(0)


offset = None
timeout = 50
chat_id: int
updates: dict
counter = 1
while True:
    print(counter)
    if offset is None:  # старт программы
        offset = -1  # -> offset + 1 = 0 -> берутся все непрочитанные сообщения

    start_time = time.time()

    # на этом место код останавливается и ждет либо истечения timeout, либо апдейта и идет дальше
    # если к этому моменту уже есть апдейты,
    # то сразу идет дальше (счетчик апдейтов сбрасывается, начинают копиться новые)
    updates = requests.get(f'{API_URL}{TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()
    # V пошли накапливаться новые апдейты

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            do_something()
    else:
        print('no updates')

    end_time = time.time()
    print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')
    counter += 1
    print('-'*50)
