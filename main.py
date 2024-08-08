import os
import time
import requests
from dotenv import load_dotenv


load_dotenv()


API_URL = 'https://api.telegram.org/bot'
TOKEN = os.getenv('BOT_TOKEN')
TEXT = 'Документы обработаны'

offset = None
counter = 0
chat_id: int

while True:
    if offset is None:  # старт программы
        offset = -1  # -> offset + 1 = 0 -> берутся все непрочитанные сообщения

    print('attempt =', counter)

    # Найдется ли апдейт с номером, следующим за предыдущим?
    # Если да, возвращает все эти апдейты т.к. offset = 322 вернет [322:]
    # Если нет, ожидание, новый цикл
    updates = requests.get(f'{API_URL}{TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        print('New updates:', len(updates['result']))
        for i, result in enumerate(updates['result']):
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')
    else:
        print('no updates')

    time.sleep(1)
    print('-'*50)
    counter += 1
