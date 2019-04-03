from BotFramework import InlineKeyboard


class Chat:

    """
    Callback query pattern: command_name-first_arg-second_arg-(...)
    List of views:
    0 - list of lists
    1 - list view
    2 - item view
    3 - user option view
    4 - list option view
    5 - item option view
    """

    def __init__(self, chat_id, bot_api):
        self.__bot_api = bot_api
        self.__current_inline_keyboard = None
        self.__last_message_id = None

        self.chat_id = chat_id
        self.current_view = None
        self.current_command = None
        self.arguments_dict = {}
        self.settings_dict = {}

    def respond(self, text, reply_markup=None):
        # Last_message_id is set to None if last message on chat is from user.
        if self.__last_message_id is not None:
            response = self.edit_message(text, self.chat_id, reply_markup)
            if response['ok'] is False:
                return self.send_message(text, reply_markup)['result']['message_id']
            else:
                self.send_chat_action('typing')
                return response
        else:
            return self.send_message(text, reply_markup)

    def send_message(self, text, reply_markup):
        assert isinstance(reply_markup, InlineKeyboard.InlineKeyboard)
        self.__current_inline_keyboard = reply_markup
        message = self.__bot_api.send_message(text, self.chat_id, reply_markup.get_keyboard_markup())
        self.__last_message_id = message['result']['message_id']
        return message

    def edit_message(self, new_text, message_id, new_reply_markup):
        assert isinstance(new_reply_markup, InlineKeyboard.InlineKeyboard)
        self.__current_inline_keyboard = new_reply_markup
        return self.__bot_api.edit_message(new_text=new_text, chat_id=self.chat_id, message_id=message_id,
                                           new_reply_markup=new_reply_markup.get_keyboard_markup())

    def send_chat_action(self, action):
        """Possible actions: 'typing', 'upload_photo', 'upload_video', 'record_video', 'upload_audio', 'record_audio',
                          'upload_document', 'find_location', 'upload_video_note', 'record_video_note'"""
        return self.__bot_api.send_chat_action(chat_id=self.chat_id, action=action)