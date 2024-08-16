import os
import traceback
from dotenv import load_dotenv

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher  # бот, диспетчер
from aiogram import F  # магический фильтр
from aiogram.filters import Command, CommandStart, CommandObject  # фильтры
from aiogram.types import Message, ContentType  # объект Message, ContentType (TEXT, PHOTO, VIDEO, etc.)

from config import config
from utils import get_unique_filename
from sql_queries import verify_guid, add_user, delete_verified_guid

load_dotenv()

API_URL = 'https://api.telegram.org/bot'
TOKEN = config['TEST_TOKEN']

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))


dp = Dispatcher()


# __________ HANDLERS __________

@dp.message(CommandStart(deep_link=True))
async def process_command_start(message: Message, command: CommandObject):
    try:
        args = command.args
        # payload = decode_payload(args)

        verification = verify_guid(args)
        new_user = add_user(message, args)
        if verification and new_user:
            delete_verified_guid(args)
            await message.answer('Успешная авторизация!')
            await message.answer(config['start_message'])
        elif verification and not new_user:
            await message.answer('Вы уже авторизованы.')
        else:
            await message.answer('Ошибка авторизации. Приглашение недействительно.'
                                 'Запросите новую ссылку-приглашение. /contacts')
    except Exception as error:
        print('Непредвиденная ошибка авторизации:', error)
        print(traceback.format_exc())
        await message.answer('Непредвиденная ошибка авторизации.')

    # print(message.model_dump_json(indent=4, exclude_none=True))


@dp.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(config['start_message'])
    # print(message.model_dump_json(indent=4, exclude_none=True))


@dp.message(Command(commands=['help']))
async def process_command_help(message: Message):
    await message.answer(config['help_message'])


@dp.message(Command(commands=['contacts']))
async def process_command_contacts(message: Message):
    await message.answer(config['contacts'])


@dp.message(F.document, lambda message: message.document.mime_type in ['application/pdf', 'image/jpeg', 'image/png'])
async def document_loader(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))
    doc = message.document
    file_name, file_id = doc.file_name, doc.file_id
    try:
        destination = get_unique_filename(os.path.join(config['save_dir'], file_name))
        await bot.download(file_id, destination)
    except Exception as error:
        print(f'Ошибка после получения документа: {error}')
        await message.answer(f"Файл \"{file_name}\" не получен.")
    else:
        await message.answer(f"Файл \"{file_name}\" успешно получен.")


@dp.message(F.document)
async def document_loader(message: Message):
    file_name = message.document.file_name
    await message.answer(f"Файл \"{file_name}\" не получен.\nНеподдерживаемый тип файла.")


@dp.message(F.photo)
async def document_loader(message: Message):
    await message.answer(f"Воспользуйтесь функцией \"Прикрепить файл\".")

    # print(message.model_dump_json(indent=4, exclude_none=True))
    # await message.answer(f"message_id:, {message.message_id}, media_group_id, {message.media_group_id}")

    # photo_id, photo_name = message.photo[-1].file_id, message.photo[-1].file_unique_id
    # try:
    #     destination = get_unique_filename(os.path.join(config['save_dir'], photo_name + '.jpg'))
    #     await bot.download(photo_id, destination)
    # except Exception as error:
    #     print(f'Ошибка после получения документа: {error}')
    #     await message.answer(f"Фото \"{photo_name}\" не получено.")
    # else:
    #     await message.answer(f"Фото \"{photo_name}\" успешно получено.")


@dp.message()
async def process_other_messages(message: Message):
    await message.answer(f"Неизвестная команда")
    print(message.model_dump_json(indent=4, exclude_none=True))


if __name__ == '__main__':
    dp.run_polling(bot, polling_timeout=7)
