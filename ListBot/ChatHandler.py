from BotAPI import InlineKeyboard


class ChatHandler:
    """
    Callback query pattern: action_name-list_id-item_id
    Possible action names:
        show_list-list_id
        add_list

    Possible chat states:
    0 - view list of lists
    1-list_id - view of list items
    """

    chat_dict = {}
    bot = None
    db = None

    @classmethod
    def initialize_class(cls, bot, db):
        cls.db = db
        cls.chat_dict = {}
        cls.bot = bot

    @classmethod
    def get_updates(cls):
        update = cls.bot.get_updates()
        for result in update['result']:

            if 'callback_query' in result:
                chat_id = result['callback_query']['message']['chat']['id']
            elif 'message' in result:
                chat_id = result['message']['chat']['id']
            else:
                continue

            if chat_id in cls.chat_dict:
                cls.chat_dict[chat_id].handle_update(result)
            else:
                message = cls.bot.send_message("List Bot", chat_id)['result']
                cls.chat_dict[chat_id] = ChatHandler(chat_id, message['message_id'], message['date'])

    def __init__(self, chat_id, message_id, message_date):
        self.chat_id = chat_id
        self.last_message_id = message_id
        self.state = 0
        self.last_message_date = message_date
        self.command = None

    def __respond(self, text, reply_markup=None, force_message=False):
        # checks if more than two days passed since last bot message and if last_message_id is set.
        # Last_message_is is none if last message was from user.
        if force_message is False and self.last_message_id is not None:
            ChatHandler.bot.edit_message(text, self.chat_id, self.last_message_id, reply_markup)
        else:
            message = ChatHandler.bot.send_message(self, text, self.chat_id, reply_markup)
            self.last_message_date = message['date']
            self.last_message_id = message['message_id']

    def handle_update(self, update):
        if "message" in update:
            self.last_message_id = None
            if 'entities' in update['message']:
                if update['message']['entities']['type'] is "bot_command":
                    self.handle_command(update['message'])
            else:
                self.handle_message(update['message'])
        elif 'callback_query' in update:
            self.handle_callback(update['callback_query'])

    def handle_message(self, message):
        pass

    def handle_callback(self, callback):
        pass

    def handle_command(self, command):
        strip = command['text'].lstrip()
        # ADD LIST
        if len(strip) >= 9 and strip[:9] is '/add_list':
            strip = strip[9:].strip()
            if len(strip) == 0:
                self.__respond(text='Enter new list name.', force_message=True)
                self.command = '/add_list'
            else:
                self.__add_list(strip)
                self.__respond(text='List "' + strip + '" has been added!')
                if self.state == 0:
                    self.show_list_of_lists()
                else:
                    ChatHandler.bot.send_chat_action(self.chat_id, 'typing')

        # SHOW LIST
        elif len(strip) >= 10 and strip[:10] is '/show_list':
            strip = strip[10:].strip()
            if len(strip) == 0 or (len(strip) == 2 and strip[0] == '"' and strip[1] == '"'):
                self.__respond(text="""Enter list number, name or ID.\n
                If list name contains only digits enter it in quotation marks.\n
                If list name is surrounded by question marks enter them twice e.g. ""name"".                
                """, force_message=True)
                self.command = '/show_list'
            else:
                if strip.isdigit():
                    strip = int(strip)
                    if strip < 100:
                        pass  # find by position number
                    else:
                        pass  # find by ID
                    # if result is empty try to find by position (theoretically position can be > 99)
                    # if result is empty inform user
                else:
                    if strip[0] == '"' and strip[0] == '"':
                        strip = strip[1:-1]
                    pass  # find list by name
                pass  # showing list
        """
        Used in or to reach state 0, when the user see list of list.
        """
    def show_list_of_lists(self):
        ik = self.__create_keyboard_markup_view_list_of_lists()
        self.__respond("Your lists:", ik)

    def __create_keyboard_markup_view_list_of_lists(self):
        tuple_of_tuples_of_id_and_name = ChatHandler.db.get_list_of_lists(self.chat_id)
        ik = InlineKeyboard.InlineKeyboard()

        for tup in tuple_of_tuples_of_id_and_name:
            ik.add_button(text=tup[0] + '. ' + tup[2], callback_data='show_list-'+tup[1], column=0)

        ik.add_button(text='Dodaj listę', callback_data='add_list', column=0)
        return ik.get_keyboard_markup()

    def __add_list(self, list_name):
        ChatHandler.db.add_list(chat_id=self.chat_id, list_name=list_name, commit=True)

        """
        Used in or to reach state 1-list_id, when the user see particular list.
        """
    def show_list_items(self, find_key):
        pass
