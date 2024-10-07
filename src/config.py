import os
import sys
import json
import requests
from dotenv import load_dotenv


config = dict()

# ____________________ PATHS ____________________

if getattr(sys, 'frozen', False):  # в сборке
    config['BASE_DIR'] = os.path.dirname(sys.executable)
else:
    config['BASE_DIR'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(config['BASE_DIR'], 'env.env'))

config['config_files'] = os.path.join(config['BASE_DIR'], 'config_files')
config['sqlite_db'] = os.path.join(config['config_files'], 'database.db')
config['codes_path'] = os.path.join(config['config_files'], 'codes.txt')

config['API_URL'] = 'https://api.telegram.org/bot'
config['TOKEN'] = os.getenv('TOKEN')

getme_url = f"https://api.telegram.org/bot{config['TOKEN']}/getMe"
config['GETME_INFO'] = requests.get(getme_url).json()

# ___ PATHS for debug (save_dir, token) ___

if __name__ == '__main__':
    DEBUG_JSON = os.path.abspath(os.path.join('..', 'DEBUG.json'))
else:
    DEBUG_JSON = os.path.abspath('DEBUG.json')

if os.path.exists(DEBUG_JSON):
    print(f"DEBUG.json was found in: {DEBUG_JSON}")
    with open(DEBUG_JSON, 'r', encoding='utf-8') as file:
        res = json.load(file)
        config['save_dir'] = os.path.abspath(res['save_dir'])
        config['TOKEN'] = res['test_token']
else:
    config['save_dir'] = r'\\10.10.0.3\docs\CUSTOM\0 Документы с Районов\IN'

config['log_folder'] = os.path.dirname(config['save_dir'])

if not os.path.exists(config['config_files']):
    os.makedirs(config['config_files'])


# ____________________ MESSAGES ____________________

config['help_message'] = """
Я работаю со следующими документами:
- Акты карантинного фитосанитарного контроля (надзора);
- Заключения о карантинном фитосанитарном состоянии;
- Протоколы исследований (испытаний).

Для отправки документа используйте кнопку 📎 "Прикрепить файл". 
Поддерживаемые форматы: <b>pdf</b>, <b>jpg</b>, <b>png</b>.

После отправки документа я сообщу о его успешном получении. Если у Вас возникли вопросы, напишите нам. /contacts
"""

config['start_message'] = f"""
👋 Добро пожаловать! Я помогу Вам отправить документы для обработки.

{config['help_message']}
"""

config['contacts'] = '\n'.join(os.getenv('contacts').split('^'))


# ____________________ SHOW CONFIG ____________________

if __name__ == '__main__':
    print('sys.frozen:', getattr(sys, 'frozen', False))
    for k, v in config.items():
        print('-' * 50)
        print(k)
        print(v)
