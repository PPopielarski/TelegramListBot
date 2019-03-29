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
    for update in bot.get_updates():
        # retrieving chat_id
        if 'callback_query' in update:
            chat_id = update['callback_query']['message']['chat']['id']
        elif 'message' in update:
            chat_id = update['message']['chat']['id']
        else:
            continue

        # creating or reading Chat instance
        if chat_id in chat_dict:
            chat = chat_dict[chat_id]
        else:
            message = bot.send_message("List Bot", chat_id)['result']
            chat = Chat(chat_id, message['message_id'], message['date'])
            chat_dict[chat_id] = chat

        # selecting appropriate handler
        if "message" in update:
            chat_dict[chat_id].last_message_id = None
            if 'entities' in update['message']:
                if update['message']['entities']['type'] is "bot_command":
                    pass  # placeholder for handling commands
            else:
                pass # placeholder for handling messages
        elif 'callback_query' in update:
            pass # placeholder for handling callback

    # end of handling updates

    # TODO placeholder for handling scheduled tasks
