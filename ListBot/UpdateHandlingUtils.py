from BotAPI import InlineKeyboard
zz

def show_list_of_lists(self):
    ik = self.__create_keyboard_markup_view_list_of_lists()
    self.__respond("Your lists:", ik)


def __create_keyboard_markup_view_list_of_lists(self):
    tuple_of_tuples_of_id_and_name = ChatHandler.db.get_list_of_lists(self.chat_id)
    ik = InlineKeyboard.InlineKeyboard()

    for tup in tuple_of_tuples_of_id_and_name:
        ik.add_button(text=tup[0] + '. ' + tup[2], callback_data='show_list-' + tup[1], column=0)

    ik.add_button(text='Dodaj listę', callback_data='add_list', column=0)
    return ik.get_keyboard_markup()


def __add_list(self, list_name):
    ChatHandler.db.add_list(chat_id=self.chat_id, list_name=list_name, commzzz