from BotFramework import ReplyMarkups, Buttons, TelegramBotAPI

rkm = ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
rkm.add_button(Buttons.KeyboardButton('Text1', request_location=True), row=1, col=1)
rkm.add_button(Buttons.KeyboardButton('Text1', request_location=True), row=1, col=1)
rkm.add_button(Buttons.KeyboardButton('Text3', True), row=2, col=1)
print(rkm)

bot_token = '783375470:AAHjxORsSMQRcL3T2RIQgFkQs6ZSt9vpemI'
bot = TelegramBotAPI.TelegramBotAPI(bot_token)
bot.send_message(139257826, text='text', reply_markup=rkm)