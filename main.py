import os
import time
import json
import requests
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher  # бот, диспетчер
from aiogram.filters import Command  # фильтры
from aiogram.types import Message, ContentType  # апдейт Message, ContentType

from config import config
from pprint import pprint


load_dotenv()

API_URL = 'https://api.telegram.org/bot'
TOKEN = os.getenv('TESTBOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()


# _____ CODE _____
# TODO: Разнести функции по хэндлерам
# TODO: Добавить проверку на наличие такого скачиваемого файлы в save_dir

# универсальный хэндлер
@dp.message()
async def document_loader(message: Message):
    # pprint(json.loads(message.json()))
    # print(message.document)
    doc = message.document
    if doc:
        file_name, file_id = doc.file_name, doc.file_id
        try:
            # Получение пути к файлу на сервере TG ->
            # -> file_id='B..' file_unique_id='A..' file_size=9.. file_path='documents/..'
            file = await bot.get_file(file_id)

            # Загрузка файла
            destination = os.path.join(config['save_dir'], file_name)
            await bot.download_file(file.file_path, destination)

        except Exception as error:
            print(f'Ошибка после получения документа: {error}')
            await message.answer(f"Файл '{file_name}' не получен.")

        else:
            await message.answer(f"Файл '{file_name}' успешно получен.")

    else:
        print('Документ не обнаружен')


if __name__ == '__main__':
    dp.run_polling(bot, polling_timeout=7)
