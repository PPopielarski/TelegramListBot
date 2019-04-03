from BotFramework import TelegramBotAPI, Chat
import time


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

    def __default_callback(self, chat, args=None):
        self.__bot_api.send_message(text="Error: callback function not recognized!", chat_id=chat.chat_id)
        self.__create_log("Error: callback function not recognized:\n" + str(args))

    def __default_command(self, chat, args=None):
        self.__bot_api.send_message(text="Command not recognised. Use /help for further assistance.",
                                    chat_id=chat.chat_id)

    def __default_message_response(self, chat, args=None):
        self.__bot_api.send_message(text="Use /help to see list of possible commands.", chat_id=chat.chat_id)

    def __init__(self, telegram_api_token, logger=None):
        self.__logger = logger
        self.__bot_api = TelegramBotAPI.TelegramBotAPI(telegram_api_token)
        self.chat_dict = {}
        self.message_handler = {}
        self.command_handler = {}
        self.callback_handler = {}
        self.__last_update_id = 0
        self.settings_dict = {}
        self.default_callback = self.__default_callback
        self.default_command = self.__default_command
        self.default_message_reaction = self.__default_message_response

    def __create_log(self, log_entry):
        if self.__logger is not None:
            self.__logger.enter_log(log_entry)

    def clear_logs(self):
        self.__logger.clear_log()
            
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
                if chat_id not in self.chat_dict:
                    self.chat_dict[chat_id] = Chat.Chat(chat_id, self.__bot_api)
                    self.chat_dict[chat_id].state = 0

                chat = self.chat_dict[chat_id]

                # selecting appropriate handler
                if "message" in update:
                    chat.last_message_id = None
                    # if user sends message then response should be new message
                    args = update['message']['text'].strip()

                    # checks if message is a command
                    if args[0] is '/':
                            args = args.split(' ', 1)
                            chat.command = None
                            self.command_handler.get(args[0], self.default_command)(chat, args)
                    else:
                        # handling messages
                        self.message_handler.get(chat.command, self.default_message_reaction)(chat, args)

                elif 'callback_query' in update:
                    args = result['callback_query']['data'].split('-')
                    self.callback_handler.get(args[0], self.default_callback)(chat, args)

                else:
                    self.__create_log('Update not recognized:\n' + str(update))

                # end of handling updates

            # TODO handling scheduled tasks

            time.sleep(0.5)
