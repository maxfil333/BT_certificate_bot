import os
import time
import requests
from dotenv import load_dotenv
from config import config


load_dotenv()

API_URL = 'https://api.telegram.org/bot'
TOKEN = os.getenv('BOT_TOKEN')

timeout = 7
offset = None
while True:
    if offset is None:  # старт программы
        offset = -1  # далее: offset + 1 = 0 и берутся все непрочитанные сообщения

    start_time = time.time()
    # На этом место код останавливается и ждет либо истечения timeout, либо апдейта и идет дальше.
    # Если к этому моменту уже есть апдейты,
    # то сразу идет дальше (счетчик апдейтов сбрасывается, начинают копиться новые)
    updates = requests.get(f'{API_URL}{TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()
    # ниже уже пошли накапливаться новые апдейты

    if updates['result']:
        n_files_received = 0
        for result in updates['result']:
            offset = result['update_id']
            message = result['message']
            chat_id = result['message']['from']['id']
            if message.get('document'):
                file_id = message['document']['file_id']
                file_name = message['document']['file_name']
                file_id_download_url = f'{API_URL}{TOKEN}/getFile?file_id={file_id}'
                file_info_response = requests.get(file_id_download_url)

                if file_info_response.status_code == 200:
                    file_info = file_info_response.json()
                    file_path = file_info['result']['file_path']
                    download_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
                    print(f'{download_url=}')

                    # Скачиваем файл
                    response = requests.get(download_url)
                    if response.status_code == 200:
                        file_save_path = os.path.join(config['save_dir'], file_name)
                        with open(file_save_path, 'wb') as f:
                            f.write(response.content)
                        print("Файл успешно скачан")
                        n_files_received += 1
                    else:
                        print(f"Ошибка загрузки файла: {response.status_code}")

        bot_reply = f'Файлов получено: {n_files_received}'
        requests.get(f'{API_URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={bot_reply}')

    else:
        print('no updates')

    end_time = time.time()
    print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')
    print('-'*50)

