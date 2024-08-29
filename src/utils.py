import os
import time
from datetime import datetime
from aiogram.types import Message
from typing import Literal

from src.logger import logger
from src.config import config


# __________ COMMON __________

def get_unique_filename(filepath):
    if not os.path.exists(filepath):
        return filepath
    else:
        base, ext = os.path.splitext(filepath)
        counter = 1
        while os.path.exists(f"{base}({counter}){ext}"):
            counter += 1
        return f"{base}({counter}){ext}"


def showlog_message_info(message: Message, message_type: Literal['file'] | Literal['authorization']):
    logger.print(datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
    try:
        if message_type == 'file':
            text = f"""
            send file:
            {message.message_id}
            {message.from_user.id}, {message.from_user.first_name}, {message.from_user.last_name}, {message.from_user.username}
            {message.document.file_name}, {message.document.mime_type}
            """
        else:
            text = f"""
            authorization:
            {message.message_id}
            {message.from_user.id}, {message.from_user.first_name}, {message.from_user.last_name}, {message.from_user.username}
            """
        logger.print(text)
    except Exception as e:
        logger.print(f'error: {e}')
        logger.print(message.model_dump_json(indent=4, exclude_none=True))

    try:
        logger.save(config['log_folder'])
        logger.clear()
    except Exception as e:
        print('showlog_message_info error:', e)
