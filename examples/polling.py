import os
import time
import requests
from dotenv import load_dotenv


load_dotenv()


API_URL = 'https://api.telegram.org/bot'
TOKEN = os.getenv('BOT_TOKEN')
TEXT = 'long pooling'

offset = None
updates: dict


def do_something() -> None:
    print('Был апдейт')


counter = 1
while True:
    print(counter)
    if offset is None:  # старт программы
        offset = -1  # -> offset + 1 = 0 -> берутся все непрочитанные сообщения

    start_time = time.time()
    updates = requests.get(f'{API_URL}{TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            do_something()

    time.sleep(3)
    print(f'Время между запросами к Telegram Bot API: {time.time() - start_time}')
    counter += 1
    print('-'*50)
