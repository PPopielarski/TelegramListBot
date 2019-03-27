from BotAPI import Bot
from DatabaseHandlers import SQLiteHandler
from ListBot import ChatHandler, Config
import time

db = SQLiteHandler.SQLiteHandler()
last_update_id = db.get_last_update_id()
if last_update_id is not None:
    bot = Bot.Bot(Config.bot_token, last_update_id)
else:
    bot = Bot.Bot(Config.bot_token)
ChatHandler.ChatHandler.initialize_class(bot, db)


while True:
    ChatHandler.ChatHandler.get_updates()
    time.sleep(1)




