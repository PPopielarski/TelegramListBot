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
                message_id = cls.bot.send_message("List Bot", chat_id)['result']['message_id']
                cls.chat_dict[chat_id] = ChatHandler(chat_id, message_id)
                cls.chat_dict[chat_id].show_list_of_lists()

    def __init__(self, chat_id, message_id):
        self.chat_id = chat_id
        self.message_id = message_id
        self.state = 0
        ChatHandler.chat_dict[chat_id] = self

    def handle_update(self, update):
        if "message" in update:
            if 'entities' in update['message']:
                if update['message']['entities']['type'] is "bot_command":
                    self.handle_command(update['message'])
            else:
                self.handle_message(update['message'])
            self.update_message(ChatHandler.bot.send_message("List Bot", self.chat_id)['result']['message_id'])
        elif 'callback_query' in update:
            self.handle_callback(update['callback_query'])

    def handle_message(self, message):
        pass

    def handle_callback(self, callback):
        pass

    def handle_command(self, command):
        if command['text'][:9] is '/add_list':
            self.__add_list(command['text'][9:])
        elif command['text'][:10] is '/show_list':
            self.__show_list(command['text'][10:])

    def update_message_id(self, new_message_id):
        ChatHandler.bot.delete_message(self.chat_id, self.message_id)
        self.message_id = new_message_id


        """
        State 0, the user see list of list.
        """

    def show_list_of_lists(self):
        ChatHandler.bot.edit_message("Listy:", self.chat_id, self.message_id,
                                     new_reply_markup=self.__create_view_list_of_lists())

    def __create_keyboard_markup_view_list_of_lists(self):
        tuple_of_tuples_of_id_and_name = ChatHandler.db.select_from_list_tab(select_list_id=True, select_list_name=True,
                                                                             where_chat_id=self.chat_id)
        ik = InlineKeyboard.InlineKeyboard()

        for tup in tuple_of_tuples_of_id_and_name:
            ik.add_button(text=tup[1], callback_data='show_list-'+tup[0], column=0)

        ik.add_button(text='Dodaj listę', callback_data='add_list', column=0)
        return ik.get_keyboard_markup()

    def __add_list(self, list_name):
        ChatHandler.db.add_list(chat_id=self.chat_id, list_name=list_name, commit=True)
        if self.state == 0:
            self.show_list_of_lists()

    """
    State 1-list_id, the user see list of list items.
    """

    def show_list_of_items(self, list_id):


    def __create_keyboard_markup_view_list(self):
        tuple_of_tuples_of_id_and_name = ChatHandler.db.select_from_list_tab(select_list_id=True, select_list_name=True,
                                                                             where_chat_id=self.chat_id)



    def __add_item(self, item_name, list_id):

