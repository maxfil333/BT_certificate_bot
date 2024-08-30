import os
import sys
from dotenv import load_dotenv

load_dotenv('env.env')

config = dict()

# ____________________ PARAMS ____________________

config['API_URL'] = 'https://api.telegram.org/bot'
config['TOKEN'] = os.getenv('TOKEN')
config['TEST_TOKEN'] = os.getenv('TEST_TOKEN')


# ____________________ PATHS ____________________

if getattr(sys, 'frozen', False):  # в сборке
    config['BASE_DIR'] = os.path.dirname(sys.executable)
else:
    config['BASE_DIR'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config['save_dir'] = r'\\10.10.0.3\docs\CUSTOM\0 Документы с Районов\IN'
config['config_files'] = os.path.join(config['BASE_DIR'], 'config_files')
config['sqlite_db'] = os.path.join(config['config_files'], 'database.db')
config['codes_path'] = os.path.join(config['config_files'], 'codes.txt')
config['log_folder'] = r'\\10.10.0.3\docs\CUSTOM\0 Документы с Районов'

if not os.path.exists(config['config_files']):
    os.makedirs(config['config_files'])


# ____________________ MESSAGES ____________________

config['help_message'] = """
Я работаю со следующими документами:
- Акты карантинного фитосанитарного контроля (надзора);
- Заключения о карантинном фитосанитарном состоянии;
- Протоколы исследований (испытаний).

Для отправки документа используйте 📎 \"Прикрепить файл\".
Поддерживаемые форматы документов: <b>pdf</b>, <b>jpg</b>, <b>png</b>.
В случае успешного получения нами Вашего документа,
Вам придет ответное сообщение.
"""
config['start_message'] = 'Привет!\n' + config['help_message']

config['contacts'] = '\n'.join(os.getenv('contacts').split('^'))


# ____________________ SHOW CONFIG ____________________

if __name__ == '__main__':
    print('sys.frozen:', getattr(sys, 'frozen', False))
    for k, v in config.items():
        print('-' * 50)
        print(k)
        print(v)
