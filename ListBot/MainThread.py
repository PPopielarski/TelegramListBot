from BotAPI import Bot
from DatabaseHandlers import SQLiteHandler
from ListBot import Chat, Config
import time

db = SQLiteHandler.SQLiteHandler(Config.sqlite_db_path)
bot = Bot.Bot(Config.bot_token)
chat_dict = {}
# getUpdates request sent in order to remove updates from time before bot was run.
bot.get_updates(timeout=0)


while True:

    # get updates from bot and loop for all of them
    for result in bot.get_updates():

        if 'callback_query' in result:
            chat_id = result['callback_query']['message']['chat']['id']
        elif 'message' in result:
            chat_id = result['message']['chat']['id']
        else:
            continue

        if chat_id in chat_dict:
            chat = chat_dict[chat_id].handle_update(result)
        else:
            message = bot.send_message("List Bot", chat_id)['result']
            chat = Chat(chat_id, message['message_id'], message['date'])
            chat_dict[chat_id] = chat


#       TODO - DOPASOWAĆ PONIŻSZĄ FUNKCJĘ DO LOOP POWŻEJ. LOOP POWINIEN JĄ WYWOŁYWAĆ DLA KAŻDEGO result.
    def handle_update(update):
        if "message" in update:
            last_message_id = None
            if 'entities' in update['message']:
                if update['message']['entities']['type'] is "bot_command":
                    handle_command(update['message'])
            else:
                handle_message(update['message'])
        elif 'callback_query' in update:
            handle_callback(update['callback_query'])


