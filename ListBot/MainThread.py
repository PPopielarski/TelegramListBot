from BotAPI import Bot
from DatabaseHandlers import SQLiteHandler
from ListBot import ChatHandler
import time


bot = Bot.Bot('783375470:AAHjxORsSMQRcL3T2RIQgFkQs6ZSt9vpemI')
db = SQLiteHandler.SQLiteHandler()
db.start()
ChatHandler.ChatHandler.initialize_class(bot, db)


while True:
    ChatHandler.ChatHandler.get_updates()
    time.sleep(1)




