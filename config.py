import os
import sys
from dotenv import load_dotenv

load_dotenv()


config = dict()

if getattr(sys, 'frozen', False):  # в сборке
    config['BASE_DIR'] = os.path.dirname(sys.executable)
    config['POPPLER_PATH'] = os.path.join(sys._MEIPASS, 'poppler')
    config['magick_exe'] = os.path.join(sys._MEIPASS, 'magick', 'magick.exe')
else:
    config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
    config['POPPLER_PATH'] = r'C:\Program Files\poppler-22.01.0\Library\bin'
    config['magick_exe'] = 'magick'  # или полный путь до ...magick.exe файла, если не добавлено в Path

config['TOKEN'] = os.getenv('TOKEN')
config['TEST_TOKEN'] = os.getenv('TEST_TOKEN')
config['save_dir'] = '__data'
# config['save_dir'] = r'\\10.10.0.3\docs\CUSTOM\0 Документы с Районов\IN'
config['config_files'] = os.path.join(config['BASE_DIR'], 'config_files')
config['sqlite_db'] = os.path.join(config['config_files'], 'database.db')

config['help_message'] = """
Я работаю со следующими документами:
- Акты карантинного фитосанитарного контроля (надзора);
- Заключения о карантинном фитосанитарном состоянии;
- Протоколы исследований (испытаний).

Для отправки документа используйте \"Прикрепить файл\".
Поддерживаемые форматы документов: <b>pdf</b>, <b>jpg</b>, <b>png</b>.
"""
config['start_message'] = 'Привет!\n' + config['help_message']

config['contacts'] = '\n'.join(os.getenv('contacts').split('^'))


if __name__ == '__main__':
    print('sys.frozen:', getattr(sys, 'frozen', False))
    for k, v in config.items():
        print('-' * 50)
        print(k)
        print(v)