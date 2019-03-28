from BotAPI import Bot
from DatabaseHandlers import SQLiteHandler
from ListBot import ChatHandler, Config
import time

db = SQLiteHandler.SQLiteHandler(Config.sqlite_db_path)
bot = Bot.Bot(Config.bot_token)
ChatHandler.ChatHandler.initialize_class(bot, db)
# getUpdates request sent in order to remove updates from time before bot was run.
bot.get_updates(timeout=0)

chat_

while True:
    ChatHandler.ChatHandler.get_updates()
    time.sleep(1)




