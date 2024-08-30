import os
import sys
from dotenv import load_dotenv


config = dict()

# ____________________ PATHS ____________________

if getattr(sys, 'frozen', False):  # в сборке
    config['BASE_DIR'] = os.path.dirname(sys.executable)
else:
    config['BASE_DIR'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(config['BASE_DIR'], 'env.env'))

config['save_dir'] = r'\\10.10.0.3\docs\CUSTOM\0 Документы с Районов\IN'
config['config_files'] = os.path.join(config['BASE_DIR'], 'config_files')
config['sqlite_db'] = os.path.join(config['config_files'], 'database.db')
config['codes_path'] = os.path.join(config['config_files'], 'codes.txt')
config['log_folder'] = r'\\10.10.0.3\docs\CUSTOM\0 Документы с Районов'

if not os.path.exists(config['config_files']):
    os.makedirs(config['config_files'])


# ____________________ PARAMS ____________________

config['API_URL'] = 'https://api.telegram.org/bot'
config['TOKEN'] = os.getenv('TOKEN')
config['TEST_TOKEN'] = os.getenv('TEST_TOKEN')


# ____________________ MESSAGES ____________________

config['help_message'] = """
Я работаю со следующими документами:
- Акты карантинного фитосанитарного контроля (надзора);
- Заключения о карантинном фитосанитарном состоянии;
- Протоколы исследований (испытаний).

Для отправки документа используйте кнопку 📎 "Прикрепить файл". 
Поддерживаемые форматы: <b>pdf</b>, <b>jpg</b>, <b>png</b>.

После отправки документа я сообщу о его успешном получении. Если у вас возникли вопросы, напишите нам /contacts.
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
