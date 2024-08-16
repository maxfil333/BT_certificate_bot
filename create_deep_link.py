import asyncio

import requests
from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link, create_deep_link

from config import config
from sql_queries import execute

TOKEN = config['TEST_TOKEN']
BOT_NAME = requests.get(f'https://api.telegram.org/bot{TOKEN}/getMe').json()['result']['username']


"""
https://docs.aiogram.dev/en/latest/utils/deep_linking.html#aiogram.utils.deep_linking.create_start_link
"""


def create_deep_link_with_guid(bot_name=BOT_NAME, guid='xxx'):
    link = create_deep_link(username=bot_name, payload=guid, link_type='start', encode=False)
    return link


def create_deep_links_from_codes(save_txt=False, show=False) -> None:
    guids = execute("SELECT guid FROM codes")
    links = [create_deep_link_with_guid(guid=guid[0]) + '\n' for guid in guids]
    if save_txt:
        with open('config_files/codes.txt', 'w', encoding='utf-8') as file:
            file.writelines(links)
    if show:
        print(*links)


async def generate_deep_link(parameter: str):
    async with Bot(token=TOKEN) as bot:
        link = await create_start_link(bot, parameter, encode=False)
        print(f'Your deep link: {link}')


if __name__ == "__main__":
    create_deep_links_from_codes(save_txt=True, show=True)
