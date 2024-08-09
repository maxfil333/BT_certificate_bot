import os
import sys
import json
import msvcrt
from glob import glob
from logger import logger
from dotenv import load_dotenv

load_dotenv()


config = dict()
config['TOKEN'] = os.getenv('BOT_TOKEN')
config['TEST_TOKEN'] = os.getenv('TESTBOT_TOKEN')
config['save_dir'] = '__data'

config['help_message'] = """
Я работаю со следующими документами:
- Акты карантинного фитосанитарного контроля (надзора);
- Заключения о карантинном фитосанитарном состоянии;
- Протоколы исследований (испытаний).

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