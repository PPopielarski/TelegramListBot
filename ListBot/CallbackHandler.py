from BotAPI import InlineKeyboard


class CallbackHandler:

    def __init__(self, bot_api, chat_dict, db):
        self.function_dict = {}
        self.bot_api = bot_api
        self.chat_dict = chat_dict
        self.db = db
        self.__populate_function_dictionary()

    def add_function(self, name, function):
        self.function_dict[name] = function

    def get_function(self, function_name):
        return self.function_dict.get(function_name)

