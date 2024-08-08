import os
import time
import requests
from dotenv import load_dotenv
from config import config


load_dotenv()

API_URL = 'https://api.telegram.org/bot'
TOKEN = os.getenv('BOT_TOKEN')
