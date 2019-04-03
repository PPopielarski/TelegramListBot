

class Chat:

    def __init__(self, chat_id, bot_api):
        self.bot_api = bot_api
        self.chat_id = chat_id
        self.last_message_id = None
        self.view = None
        self.command = None
        self.arguments_dict = {}
        self.settings_dict = {}

    def respond(self, text, reply_markup=None, force_message=False):
        # checks if more than two days passed since last bot message and if last_message_id is set.
        # Last_message_is is none if last message was from user.
        if force_message is False and self.last_message_id is not None:
            response = self.bot_api.edit_message(text, self.chat_id, reply_markup)
            if response['ok'] is False:
                message = self.bot_api.send_message(text, self.chat_id, reply_markup)
                self.last_message_id = message['result']['message_id']
            else:
                self.bot_api.send_chat_action(self.chat_id, 'typing')
        else:
            message = self.bot_api.send_message(text, self.chat_id, reply_markup)
            self.last_message_id = message['result']['message_id']
