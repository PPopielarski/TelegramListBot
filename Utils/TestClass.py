from BotFramework import ReplyMarkups, Buttons, TelegramBotAPI

key = ReplyMarkups.InlineKeyboardMarkup
key.pop_button(col=1, row=1)

bot_token = '783375470:AAHjxORsSMQRcL3T2RIQgFkQs6ZSt9vpemI'
bot = TelegramBotAPI.TelegramBotAPI(bot_token)
x = bot.send_message(139257826, text='text')
print(type(x))
print(x)
