from aiogram import Bot, Dispatcher  # бот, диспетчер
from aiogram.client.default import DefaultBotProperties

from src import handlers
from src.config import config
from src.create_db import main as main_create_db
from src.create_deep_link import create_deep_links_from_codes


# __________ BOT PARAMETERS __________

TOKEN = config['TOKEN']
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

# _______________ MAIN _______________

if __name__ == '__main__':
    dp.run_polling(bot, polling_timeout=7)
