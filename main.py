import asyncio
import argparse
from aiogram import Bot, Dispatcher  # бот, диспетчер
from aiogram.client.default import DefaultBotProperties

from src import handlers
from src.config import config
from src.create_db import main as main_create_db
from src.create_deep_link import create_deep_links_from_codes


async def main(production=False):
    # TODO: убрать production

    print(f'prod: {production}')

    # ____________ TOKEN ____________
    TOKEN = config['TOKEN']

    # __________ BOT PARAMETERS __________
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

    # _____________ DATABASE _____________
    # load or create DB
    main_create_db()
    # export current available codes from db to file
    create_deep_links_from_codes(token=TOKEN, save_txt=True)

    # ____________ DISPATCHER ____________
    dp = Dispatcher()
    dp.include_router(handlers.authorization_router)
    dp.include_router(handlers.router)

    await dp.start_polling(bot, polling_timeout=7)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="DESCRIPTION: BT_certificate_bot")
    parser.add_argument('-p', '--production', action='store_true', help='production run')
    args = parser.parse_args()

    asyncio.run(main(production=args.production))
