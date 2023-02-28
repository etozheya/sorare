import requests

from tg_bot.vars import bot_token, offer_channel_id, auction_channel_id


def send_offer_message(text):
    requests.post(
        url=f'https://api.telegram.org/bot{bot_token}/sendMessage',
        json={'chat_id': offer_channel_id, 'text': text})


def send_auction_message(text):
    requests.post(
        url=f'https://api.telegram.org/bot{bot_token}/sendMessage',
        json={'chat_id': auction_channel_id, 'text': text})
