import requests
from pprint import pprint
from dotenv import load_dotenv

from src.config import config


load_dotenv()

API_URL = 'https://api.telegram.org/bot'
TOKEN = config['TEST_TOKEN']


def print_response(response):
    if response.status_code == 200:
        pprint(response.json())
    else:
        print(response.status_code)


getme_url = f'https://api.telegram.org/bot{TOKEN}/getMe'
get_updates_url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'

if __name__ == "__main__":
    print('getMe:')
    print(f'url: {getme_url}')
    print_response(requests.get(getme_url))
    print('-' * 50)

    print('getUpdates:')
    print(f'url: {get_updates_url}')
    print_response(requests.get(get_updates_url))
    print('-' * 50)
