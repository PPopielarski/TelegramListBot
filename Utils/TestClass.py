from BotFramework import ReplyMarkups, Buttons, TelegramBotAPI

rkm = ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
rkm.add_button(Buttons.KeyboardButton('Text1', request_location=True), row=1, col=1)
rkm.add_button(Buttons.KeyboardButton('Text2', True), row=1, col=2)
rkm.add_button(Buttons.KeyboardButton('Text3', True), row=2, col=1)
print(rkm.get_markup())

bot_api = TelegramBotAPI.TelegramBotAPI('783375470:AAHjxORsSMQRcL3T2RIQgFkQs6ZSt9vpemI')

bot_api.send_message(chat_id=139257826, text='text', reply_markup=rkm.get_markup())
