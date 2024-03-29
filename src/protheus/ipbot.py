import requests
import json


def get_settings(key):
    with open('settings.json') as json_file:
        data = json.load(json_file)
        if key in data:
            return [True, data[key]]
        else:
            return [False]


def set_config(self, key, value):
    conf = {}
    with open('settings.json') as json_file:
        conf = json.load(json_file)
        conf.update(dict({key: value}))
        with open('settings.json', 'w') as json_read:
            json.dump(conf, json_read, indent=4)

        print(
            f'Arquivo de configuração alterado | chave: {key} , valor: {value}')

        return conf


def bot_protheus(bot_message):

    bot_info = get_settings('bot')

    if bot_info[0]:
        bot_token = bot_info[1].get('bot_token', None)
        bot_chatID = bot_info[1].get('bot_chatid', None)
    else:
        print('Configure as chaves bot_token e bot_chatid')
        return

    if bot_chatID is not None or bot_token is not None:
        send_text = 'https://api.telegram.org/bot' + bot_token + \
            '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()
    else:
        print('Configure as chaves bot_token e bot_chatid')
    return


def get_group_id():

    chats: list = []
    all_chats: list = []
    bot_info = get_settings('bot')

    if bot_info[0]:
        bot_token = bot_info[1].get('bot_token', None)
    else:
        print('Configure as chaves bot_token e bot_chatid')
        return

    get_groups = f'https://api.telegram.org/bot{bot_token}/getUpdates'

    response = requests.get(get_groups)

    data = response.json()

    if not data['ok']:
        print(data['description'])
        return []

    for d in data['result']:
        try:
            id_chat = d['message']['chat']['id']
        except KeyError:
            id_chat = d['edited_message']['chat']['id']

        if id_chat in chats:
            continue

        chats.append(id_chat)

        type_chat = d['message']['chat']['type']

        if type_chat == 'group':
            chat_name = d['message']['chat'].get('title', '')
        else:
            chat_name = d['message']['chat'].get('first_name', '')

        id_name = d['message']['from'].get('id', '')
        first_name = d['message']['from'].get('first_name')
        # text = d['message'].get('text', '')

        all_chats.append({"user_id": id_name, "nome": first_name, "tipo": type_chat, "id_chat": id_chat, "chat_name": chat_name})

    return all_chats


if __name__ == "__main__":
    msg = ""
    bot_protheus(f'Alguem sabe pq me fui chamado pela classe {__name__} ?')
