from BotAPI import BotAPI
from DatabaseHandlers import SQLiteHandler
from ListBot import Chat, Config, CommandHandler, Logger
import time

logger = Logger.Logger()
db = SQLiteHandler.SQLiteHandler(Config.sqlite_db_path, logger)
bot_api = BotAPI.BotAPI(Config.bot_token)
chat_dict = {}
bot_api.get_updates(timeout=1)
# message_handler = MessageHandler.get()
command_handler = CommandHandler.CommandHandler(bot_api, chat_dict, db)
# callback_handler = CallbackHandler.get()
# getUpdates request sent in order to remove updates sent before bot was run.


while True:

    # get updates from bot and loop for all of them
    for update in bot_api.get_updates()['result']:
        # retrieving chat_id
        if 'callback_query' in update:
            chat_id = update['callback_query']['message']['chat']['id']
        elif 'message' in update:
            chat_id = update['message']['chat']['id']
        else:
            logger.enter_log("Update not recognised:\n" + str(update))
            continue

        # creating chat instance if necessary
        if chat_id not in chat_dict:
            chat_dict[chat_id] = Chat.Chat(chat_id, bot_api)
            chat_dict[chat_id].state = 0

        # selecting appropriate handler
        if "message" in update:
            chat_dict[chat_id].last_message_id = None  # if user sends message then response should be new message
            text = update['message']['text'].strip()
            if text.split(' ', 1)[0][0] is '/':  # checks if message is a command
                    text = text.split(' ', 1)
                    chat_dict[chat_id].command = None
                    if len(text) == 2:
                        command_handler.get_function(text[0].split())(chat_id, text[1].split())
                    else:
                        command_handler.get_function(text[0].split())(chat_id, '')
            else:
                pass # placeholder for handling messages
        elif 'callback_query' in update:
            pass  # placeholder for handling callback

    # end of handling updates

    # TODO handling scheduled tasks

    time.sleep(0.5)
