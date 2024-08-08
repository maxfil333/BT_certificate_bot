# code example from https://stepik.org/lesson/759399/step/1?unit=761415


import os
import requests
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command  # фильтры
from aiogram.types import Message, ContentType  # апдейт Message, ContentType
from aiogram import F  # Магический фильтр

load_dotenv()
BOT_TOKEN = os.getenv('TESTBOT_TOKEN')

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def presp(response):
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.status_code)


# Этот хэндлер будет срабатывать на команду "/start"
# задекорированная асинхронная функция, принимающая на вход объект типа Message,
# если срабатывает фильтр в декораторе (через фильтр Command(commands=["start"] пройдет только команда /start)
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')  # ответ в этот чат
    # await bot.send_message(message.chat.id, message.text)  # то же самое
    # await bot.send_message(chat_id='ID или название чата', text='Какой-то текст')  # ответ в другой чат


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


# Этот хэндлер будет срабатывать на отправку боту фото
@dp.message(F.photo)
async def send_photo_echo(message: Message):
    # print(message)
    await message.reply_photo(message.photo[0].file_id)


# Этот хэндлер будет срабатывать на любые ваши (текстовые и не только) сообщения,
# кроме команд "/start" и "/help"
# Хэндлер зарегистрирован позже остальных, чтобы не перехватывал другие команды
# @dp.message()
# async def send_echo(message: Message):
#     print(11111111111111)
#     await message.reply(text=message.text)  # reply - этот метод подразумевает, что у апдейта есть поле text


# универсальный хэндлер
@dp.message()
async def send_echo(message: Message):
    print(2222222222222)
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )


# _______________________ Способ регистрации хэндлеров без декораторов _________________________________________________
"""
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')

async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ '
                         'я пришлю тебе твое сообщение')

async def send_photo_echo(message: Message):
    print(message)
    await message.reply_photo(message.photo[0].file_id)

async def send_echo(message: Message):
    await message.reply(text=message.text)

# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(send_echo)
dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)  # AUDIO | VOICE | DOCUMENT 
# dp.message.register(send_photo_echo, F.photo)  # audio | voice | document

"""

# ______________________________________________________________________________________________________________________


if __name__ == '__main__':
    dp.run_polling(bot, polling_timeout=7)
    # getupdates_url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    # print(getupdates_url)
    # response = requests.get(getupdates_url)
    # presp(response)
