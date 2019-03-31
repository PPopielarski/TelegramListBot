from BotAPI import InlineKeyboard


class CommandHandler:

    def __init__(self, bot, chat_dict, db):
        self.function_dict = {}
        self.bot = bot
        self.chat_dict = chat_dict
        self.db = db
        self.__populate_function_dictionary()

    def add_function(self, name, function):
        self.function_dict[name] = function

    def get_function(self, function_name):
        return self.function_dict.get(function_name)

    def __add_list(self, chat_id, arguments):
            if len(arguments) == 0:
                self.chat_dict[chat_id].respond(text='Enter new list name.', force_message=True)
                self.chat_dict[chat_id].command = '/add_list'
            else:
                self.db.add_list(chat_id=chat_id, list_name=arguments)
                self.chat_dict[chat_id].respond(text='List "' + arguments + '" has been added!')
                if self.chat_dict[chat_id].state == 0:
                    self.function_dict['/show_lists'](chat_id, '')
                else:
                    self.bot.send_chat_action(chat_id, 'typing')

    def __show_lists_of_lists(self, chat_id, arguments):
        if arguments is 'all':
            tuple_of_tuples = self.db.get_list_of_lists(self.chat_dict[chat_id].chat_id, deleted=None)
        elif arguments is 'deleted':
            tuple_of_tuples = self.db.get_list_of_lists(self.chat_dict[chat_id].chat_id, deleted=True)
        else:
            tuple_of_tuples = self.db.get_list_of_lists(self.chat_dict[chat_id].chat_id, deleted=False)

        ik = InlineKeyboard.InlineKeyboard()

        i = 1
        for tup in tuple_of_tuples:
            ik.add_button(text=str(i) + '. ' + str(tup[1]), callback_data='show_list-' + str(tup[0]), column=0)
            i = i + 1

        ik.add_button(text='Dodaj listę', callback_data='add_list', column=0)
        self.chat_dict[chat_id].respond("Your lists:", ik)
        self.chat_dict[chat_id].state = 0

    def __populate_function_dictionary(self):
        self.add_function('/add_list', self.__add_list)
        self.add_function('/show_lists', self.__show_lists_of_lists)
