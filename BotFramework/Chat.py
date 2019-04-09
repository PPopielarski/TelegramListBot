import time
from BotFramework import TelegramBotAPI, Bot


class Chat:

    __slots__ = '__bot_api', '__current_inline_keyboard', '__last_message_id', 'chat_id', 'current_view', \
                'current_command', 'last_usage_time', 'on_delete_function', '__current_reply_keyboard'

    def __init__(self, chat_id: int, bot_api: TelegramBotAPI.TelegramBotAPI, on_delete_function=None):
        self.__bot_api = bot_api
        self.__current_inline_keyboard = None
        self.__current_reply_keyboard = None
        self.__last_message_id = None

        self.chat_id = chat_id
        self.current_view = None
        self.current_command = None
        self.last_usage_time = time.time()
        self.on_delete_function = on_delete_function

    def call_on_delete_function(self, chat, bot, bot_api):
        if self.on_delete_function is not None:
            self.on_delete_function(chat, bot, bot_api)

    def respond(self, text, reply_markup=None) -> dict:
        # Last_message_id is set to None if last message on chat is from user.
        if self.__last_message_id is not None:
            response = self.edit_message(text, self.chat_id, reply_markup)
            if response['ok'] is False:
                return self.send_message(text, reply_markup)['result']['message_id']
            else:
                self.__bot_api.send_chat_action(self.chat_id, 'typing')
                return response
        else:
            return self.send_message(text, reply_markup)

    def send_message(self, text, reply_markup=None) -> dict:
        self.__current_inline_keyboard = reply_markup
        message = self.__bot_api.send_message(text=text, chat_id=self.chat_id,
                                              reply_markup=reply_markup.get_keyboard_markup())
        self.__last_message_id = message['result']['message_id']
        return message

    def edit_message(self, new_text, message_id, new_reply_markup=None) -> dict:
        self.__current_inline_keyboard = new_reply_markup
        return self.__bot_api.edit_message_text(new_text=new_text, chat_id=self.chat_id, message_id=message_id,
                                                new_reply_markup=new_reply_markup.get_keyboard_markup())
