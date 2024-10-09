import requests
from pprint import pprint

from src.config import config


def print_response(response):
    if response.status_code == 200:
        pprint(response.json())
    else:
        print(response.status_code)


if __name__ == "__main__":
    API_URL = config['API_URL']
    TOKEN = config['TOKEN']

    getMe = f'https://api.telegram.org/bot{TOKEN}/getMe'
    getUpdates = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    getWebhookInfo = f'https://api.telegram.org/bot{TOKEN}/getWebhookInfo'

    print('getMe:')
    print(f'url: {getMe}')
    print_response(requests.get(getMe))
    print('-' * 50)

    print('getUpdates:')
    print(f'url: {getUpdates}')
    print_response(requests.get(getUpdates))
    print('-' * 50)

    print('getWebhookInfo:')
    print(f'url: {getWebhookInfo}')
    print_response(requests.get(getWebhookInfo))
    print('-' * 50)
