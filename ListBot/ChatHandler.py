from BotAPI import InlineKeyboard


class ChatHandler:
    """
    Callback query pattern: action_name-list_id-item_id
    Possible action names:
        view_list-list_id
        add_list

    Possible chat states:
    0 - view list of lists
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
                cls.bot.edit_message("Listy:", chat_id, message_id,
                                     new_reply_markup=cls.chat_dict[chat_id].__create_view_list_of_lists())

    def __init__(self, chat_id, message_id):
        self.chat_id = chat_id
        self.message_id = message_id
        self.state = 0
        ChatHandler.chat_dict[chat_id] = self

    def handle_update(self, update):
        if "message" in update:
            pass

    def handle_message(self, message):
        pass

    def handle_callback(self, callback):
        pass

    def __create_view_list_of_lists(self):
        tuple_of_tuples_of_id_and_name = ChatHandler.db.select_from_list_tab(select_list_id=True, select_list_name=True,
                                                                             where_chat_id=self.chat_id)
        ik = InlineKeyboard.InlineKeyboard()

        for tup in tuple_of_tuples_of_id_and_name:
            ik.add_button(text=tup[1], callback_data='view_list-'+tup[0], column=0)

        ik.add_button(text='Dodaj listę', callback_data='add_list', column=0)
        return ik.get_keyboard_markup()
