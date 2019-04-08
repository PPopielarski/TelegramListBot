from BotFramework import ReplyMarkups, Buttons, TelegramBotAPI
import time

bot_token = '783375470:AAHjxORsSMQRcL3T2RIQgFkQs6ZSt9vpemI'
bot = TelegramBotAPI.TelegramBotAPI(bot_token)

ik = ReplyMarkups.InlineKeyboardMarkup()
ik.add_button(Buttons.InlineKeyboardButton('przycisk', callback_data='cbd'), row=1, col=1)

bot.send_message(chat_id=139257826, text='text_przycisk', reply_markup=ik)

time.sleep(4)

updates = bot.get_updates()

for result in updates['result']:
    print(result)
    cal_id = result['callback_query']['id']

bot.answer_callback_query(callback_query_id=cal_id, text='False', show_alert=False, cache_time=10)
