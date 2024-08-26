from dotenv import load_dotenv

from aiogram import Bot, Dispatcher  # бот, диспетчер
from aiogram.client.default import DefaultBotProperties

import handlers
from config import config
from create_db import main as main_create_db
from create_deep_link import create_deep_links_from_codes

load_dotenv()


# _____________ DATABASE _____________

# load or create DB
main_create_db()

# export current available codes to file
create_deep_links_from_codes(save_txt=True)


# __________ BOT PARAMETERS __________

TOKEN = config['TEST_TOKEN']
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
dp.include_router(handlers.authorization_router)
dp.include_router(handlers.router)


# _______________ MAIN _______________

if __name__ == '__main__':
    dp.run_polling(bot, polling_timeout=7)
