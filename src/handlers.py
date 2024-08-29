import os
import traceback

from aiogram import Bot  # бот
from aiogram import Router  # роутер
from aiogram import F  # магический фильтр
from aiogram.filters import Command, CommandStart, CommandObject  # фильтры
from aiogram.types import Message, ContentType  # объект Message, ContentType (TEXT, PHOTO, VIDEO, etc.)

from src.config import config
from src.filters import IsAuthorizedUser
from src.utils import get_unique_filename, showlog_message_info
from src.sql_queries import is_in_codes, add_user, delete_verified_guid, is_in_users


# ___________ ROUTERS ___________

# Инициализируем роутер попытки регистрации; Добавляем фильтр на команду start (по ссылке)
authorization_router = Router()
authorization_router.message.filter(CommandStart(deep_link=True))

# Инициализируем роутеры уровня модуля; Добавляем фильтр наличия доступа у пользователя
router = Router()
router.message.filter(IsAuthorizedUser())


# __________ HANDLERS __________

@authorization_router.message()
async def process_command_start(message: Message, command: CommandObject):
    try:
        argument = command.args  # type(argument) is str
        user_verified = is_in_users(message)
        if user_verified:
            await message.answer('Вы уже авторизованы.')
        else:
            guid_verified = is_in_codes(guid=argument)
            if guid_verified:
                add_user(message=message, guid=argument)
                delete_verified_guid(guid=argument)
                await message.answer('Успешная авторизация!')
                await message.answer(config['start_message'])
                showlog_message_info(message, message_type='authorization')
            else:
                await message.answer('Ошибка авторизации. Приглашение недействительно.'
                                     'Запросите новую ссылку-приглашение. /contacts')

    except Exception as error:
        print('Непредвиденная ошибка авторизации:', error)
        print(traceback.format_exc())
        await message.answer('Непредвиденная ошибка авторизации.')

    # print(message.model_dump_json(indent=4, exclude_none=True))


@router.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(config['start_message'])
    # print(message.model_dump_json(indent=4, exclude_none=True))


@router.message(Command(commands=['help']))
async def process_command_help(message: Message):
    await message.answer(config['help_message'])


@router.message(Command(commands=['contacts']))
async def process_command_contacts(message: Message):
    await message.answer(config['contacts'])


@router.message(F.document, lambda message: message.document.mime_type in ['application/pdf', 'image/jpeg', 'image/png'])
async def document_loader(message: Message, bot: Bot):
    showlog_message_info(message, message_type='file')
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


@router.message(F.document)
async def document_loader(message: Message):
    file_name = message.document.file_name
    await message.answer(f"Файл \"{file_name}\" не получен.\nНеподдерживаемый тип файла.")


@router.message(F.photo)
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


@router.message()
async def process_other_messages(message: Message):
    await message.answer(f"Неизвестная команда")
    # print(message.model_dump_json(indent=4, exclude_none=True))
