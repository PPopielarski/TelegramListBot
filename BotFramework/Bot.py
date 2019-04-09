from BotFramework import TelegramBotAPI, Chat, TxtLogger
import time
import inspect

# TODO on delete function - think what argument should it take, 
# TODO and for what types of chats should they be applied
# TODO Consider replace setting configurations by functions by generating chat prototypes and inserting them into
# TODO bot while it's created


class Bot:
    """
    Callback query pattern: command_name-first_arg-second_arg-(...)
    Typical: command_name-view_number-list_id-item_id

    List of views:
    0 - list of lists
    1 - list view
    2 - item view
    3 - user option view
    4 - list option view
    5 - item option view

    """

    def __default_callback(self, chat, update):
        self.__bot_api.send_message(text="Error: callback function not recognized!", chat_id=chat.chat_id)
        self.__create_log("Error: callback function not recognized:\n" + str(update))

    def __default_command(self, chat, _):
        self.__bot_api.send_message(text="Command not recognised. Use /help for further assistance.",
                                    chat_id=chat.chat_id)

    def __default_message_response(self, chat, _):
        self.__bot_api.send_message(text="Use /help to see list of possible commands.", chat_id=chat.chat_id)

    def __init__(self, telegram_api_token: str, chat_on_delete_function, chat_life_time: int = 600,
                 logger: TxtLogger.TxtLogger = None):
        assert isinstance(telegram_api_token, str)
        assert chat_life_time is None or (isinstance(chat_life_time, int) and chat_life_time > 0)
        assert logger is None or isinstance(logger, TxtLogger.TxtLogger)

        self.__chat_on_delete_function = chat_on_delete_function
        self.__logger = logger
        self.__bot_api = TelegramBotAPI.TelegramBotAPI(telegram_api_token)
        self.__message_handler = {}
        self.__command_handler = {}
        self.__callback_handler = {}
        self.__last_update_id = 0
        self.__default_callback = self.__default_callback
        self.__default_command = self.__default_command
        self.__default_message_reaction = self.__default_message_response
        self.__chat_dict = {}
        self.__chat_life_time = chat_life_time

    def __create_log(self, log_entry):
        if self.__logger is not None:
            self.__logger.enter_log(log_entry)

    def set_chat_on_delete_function(self, func):
        assert hasattr(func, '__call__'), "Argument func must be a function with argument (chat, bot, bot_api)."
        self.__chat_on_delete_function = func

    def get_chat_life_time(self):
        return self.__chat_life_time

    def set_chat_life_time(self, chat_life_time: int):
        assert chat_life_time is None or (isinstance(chat_life_time, int) and chat_life_time > 0)
        self.__chat_life_time = chat_life_time

    def pop_callback_function(self, name: str):
        return self.__callback_handler.pop(name)

    def pop_command_function(self, name: str):
        return self.__command_handler.pop(name)

    def pop_message_reaction_function(self, name: str):
        return self.__message_handler.pop(name)

    def add_callback_function(self, name: str, func):
        assert hasattr(func, '__call__'), "Argument func must be function with argument (update)."
        assert inspect.signature(func) == '(update)'
        assert isinstance(name, str)
        if name not in self.__callback_handler:
            self.__callback_handler[name] = func
            return True
        else:
            raise Exception('Name already in use!')

    def add_command_function(self, name: str, func):
        assert hasattr(func, '__call__'), "Argument func must be function with argument (update)."
        assert inspect.signature(func) == '(update)'
        assert isinstance(name, str)
        if name not in self.__callback_handler:
            self.__command_handler[name] = func
            return True
        else:
            raise Exception('Name already in use!')

    def add_message_reaction_function(self, name: str, func):
        assert hasattr(func, '__call__'), "Argument func must be function with argument (update)."
        assert inspect.signature(func) == '(update)'
        assert isinstance(name, str)
        if name not in self.__callback_handler:
            self.__message_handler[name] = func
            return True
        else:
            raise Exception('Name already in use!')

    def set_default_callback_response(self, func):
        assert hasattr(func, '__call__')
        self.__default_callback = func

    def set_default_command_response(self, func):
        assert hasattr(func, '__call__')
        self.__default_command = func

    def set_default_message_response(self, func):
        assert hasattr(func, '__call__')
        self.__default_message_reaction = func

    def clear_logs(self):
        if self.__logger is not None:
            self.__logger.clear_logs()

    def get_updates(self, offset: int, timeout: int = 100):
        return self.__bot_api.get_updates(offset, timeout)

    def get_bot_details(self):
        return self.__bot_api.get_me()

    def start(self):

        update = self.__bot_api.get_updates(timeout=1, offset=0)
        # getUpdates request sent in order to remove updates sent before bot was run.
        for result in update:
            if int(result['update_id']) > self.__last_update_id:  # updating update_id to create offset
                self.__last_update_id = int(result['update_id'])

        while True:

            # get updates from bot and loop for all of them
            for result in self.__bot_api.get_updates(offset=self.__last_update_id + 1)['result']:
                if int(result['update_id']) > self.__last_update_id:  # updating update_id to create offset
                    self.__last_update_id = int(result['update_id'])

                # reading chat_id
                if 'callback_query' in result:
                    chat_id = result['callback_query']['message']['chat']['id']
                elif 'message' in update:
                    chat_id = result['message']['chat']['id']
                else:
                    self.__create_log("Update not recognised:\n" + str(result))
                    continue

                # creating chat instance if necessary
                if chat_id not in self.__chat_dict:
                    chat = Chat.Chat(chat_id, self.__bot_api, self.__chat_on_delete_function)
                    self.__chat_dict[chat_id] = chat
                else:
                    chat = self.__chat_dict[chat_id]
                    chat.last_usage_time = time.time()

                # selecting appropriate handler
                if "message" in update:
                    chat.last_message_id = None
                    # if user sends message then response should be new message
                    args = update['message']['text'].strip()

                    # checks if message is a command
                    if args[0] is '/':
                            args = args.split(' ', 1)
                            chat.command = None
                            self.__command_handler.get(args[0], self.__default_command)(chat, args)

                    else:
                        # handling messages
                        self.__message_handler.get(chat.command, self.__default_message_reaction)(chat, args)

                elif 'callback_query' in update:
                    args = result['callback_query']['data'].split('-')
                    self.__callback_handler.get(args[0], self.__default_callback)(chat, args)

                else:
                    self.__create_log('Update not recognized:\n' + str(update))

                # end of handling updates

            # TODO handling scheduled tasks

            # delete unused chats from dictionary
            if self.__chat_life_time is not None:
                for chat_id in self.__chat_dict:
                    if time.time() - self.__chat_dict[chat_id].last_usage_time > self.__chat_life_time:
                        self.__chat_dict[chat_id].call_on_delete_function()
                        del self.__chat_dict[chat_id]

            time.sleep(0.5)
