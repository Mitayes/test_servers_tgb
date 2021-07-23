import requests
from test_servers_config import api_token, chat_id


def bot_send_photo(image, chat):
    photo = {'photo': open(image, 'rb')}
    data = {'chat_id': chat}
    requests.post(f'https://api.telegram.org/bot{api_token}/sendPhoto', files=photo, data=data)


def bot_send_message(message, chat):
    data = {
        'chat_id': chat,
        'text': message,
    }
    requests.get(f'https://api.telegram.org/bot{api_token}/sendMessage', params=data)


# example using def 'bot_send_message'
# bot_send_message('test message', chat_id)

# example using def 'bot_send_photo'
# bot_send_photo(img_file, chat_id)
