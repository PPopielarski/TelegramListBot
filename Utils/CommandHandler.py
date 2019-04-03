from BotFramework.reply_markup import InlineKeyboard


class CommandHandler:

    def __init__(self, bot_api, chat_dict, db):
        self.function_dict = {}
        self.bot_api = bot_api
        self.chat_dict = chat_dict
        self.db = db
        self.__populate_function_dictionary()

    def add_function(self, name, f):
        self.function_dict[name] = f

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
                    self.bot_api.send_chat_action(chat_id, 'typing')

    def __show_lists_of_lists(self, chat_id, arguments):
        if arguments is 'all':
            tuple_of_tuples = self.db.get_list_of_lists(self.chat_dict[chat_id].chat_id, deleted=None)
        elif arguments is 'deleted':
            tuple_of_tuples = self.db.get_list_of_lists(self.chat_dict[chat_id].chat_id, deleted=True)
        else:
            tuple_of_tuples = self.db.get_list_of_lists(self.chat_dict[chat_id].chat_id, deleted=False)

        ik = InlineKeyboard.InlineKeyboard()

        for tup in tuple_of_tuples:
            ik.add_button(text=str(tup[2]) + '. ' + str(tup[1]), callback_data='show_list-' + str(tup[0]), column=0)

        ik.add_button(text='Dodaj listę', callback_data='add_list', column=0)
        self.chat_dict[chat_id].respond("Your lists:", ik)
        self.chat_dict[chat_id].state = 0

    def __delete_list(self, chat_id, arguments):
        if arguments == '' or (len(arguments) == 2 and arguments[0] == '"' and arguments[-1] == '"'):
            self.chat_dict[chat_id].respond('''Enter list number, name or ID.\n
                If list name contains only digits enter it in quotation marks.\n
                If list name is surrounded by question marks enter them twice e.g. ""name""''', force_message=True)
            self.chat_dict[chat_id].command = '/delete_list'
        if arguments.isdigit():
            arguments = int(arguments)
            if arguments > 99:
                success = self.db.delete_list_by_id(chat_id, list_id=arguments)
                if success:
                    self.chat_dict[chat_id].respond("List with ID " + str(arguments) + " deleted.")
                    return success
            else:
                success = self.db.delete_list_by_position(chat_id, position=arguments)
                if success:
                    self.chat_dict[chat_id].respond("List on position " + str(arguments) + " deleted.")
                    return success
            if not success and arguments > 99:
                success = self.db.delete_list_by_position(chat_id, position=arguments)
                if success:
                    self.chat_dict[chat_id].respond("List on position " + str(arguments) + " deleted.")
                else:
                    self.chat_dict[chat_id].respond("List with specified ID or position could not be found.")
            return success
        else:
            if arguments[0] == '"' and arguments[-1] == '"':
                arguments = arguments[1:-1]
            success = self.db.delete_list_by_name(chat_id, list_name=arguments)
            if success:
                self.chat_dict[chat_id].respond('List with name "' + arguments + '" deleted.')
            else:
                self.chat_dict[chat_id].respond('List with name "' + arguments + '" could not be found.')
            return success

    def __rename_list(self, chat_id, arguments):
        if len(arguments.split(' ')) == 0:
            self.chat_dict[chat_id].respond('''Enter list number, name or ID and then new name, e.g. 12 <new_name>"\n
                You can specify the list by name by surrounding arguments it with quotation marks ("), e.g. "old name" 
                "new name".\n
                If new name contains only digits enter it in quotation marks (").\n
                If list name is surrounded by question marks enter them twice e.g. ""new name"".\n
                Send /cancel to stop the procedure.''', force_message=True)
            self.chat_dict[chat_id].command = '/list.rename'
            return False
        if len(arguments.split(' ')) == 1:
            arguments = arguments.strip()
            self.chat_dict[chat_id].command = '/list.rename'
            if arguments.isdigit():
                arguments = int(arguments)
                self.chat_dict[chat_id].arguments_dict['number'] = arguments
                self.chat_dict[chat_id].respond('Enter new name for list with position/ID = ' + str(arguments) + '.\n' +
                                                'Send /cancel to stop the procedure.', force_message=True)
            else:
                list_id = self.db.get_list_id_by_name(chat_id, arguments)
                if len(list_id) == 0:
                    self.chat_dict[chat_id].respond(
                        'List with specified name is not found. If "' + arguments +
                        '''" is desired new name of list specify the list by providing it`s name, ID or position or
                        send /cancel to stop the procedure.''', force_message=True)
                    self.chat_dict[chat_id].command = '/list.rename'
                    self.chat_dict[chat_id].arguments_dict['new_name'] = arguments
                elif len(list_id) == 1:
                    self.chat_dict[chat_id].respond(
                        'List with specified name was found. If "' + arguments +
                        '''" is list you want to rename send it`s new name or send /cancel to stop the procedure.''',
                        force_message=True)
                    self.chat_dict[chat_id].command = '/list.rename'
                    self.chat_dict[chat_id].arguments_dict['list_id'] = list_id[0]
                else:
                    self.chat_dict[chat_id].respond('More than one list with specified name were found. ' +
                                                    'If "' + arguments + '''" is a new name you want to apply for some 
                                                    list send it`s position or ID or send /cancel to stop the procedure.
                                                    ''',  force_message=True)
                self.chat_dict[chat_id].arguments_dict['new_name'] = arguments.strip()
                self.chat_dict[chat_id].command = '/list.rename'
        if arguments.split(' ', 1)[0].strip().isdigit():
            number = int(arguments.split(' ', 1)[0].strip())
            new_name = arguments.split(' ', 1)[1].strip()
            if new_name[0] == '"' and new_name[-1] == '"':
                new_name = new_name[1:-1]
            if number > 99:
                success = self.db.rename_list_by_id(chat_id, number, new_name)
                if success:
                    self.chat_dict[chat_id].respond('List with ID ' + str(number) + ' renamed as "' + new_name + '".')
                    return success
            else:
                success = self.db.rename_list_by_position(chat_id, number, new_name)
                if success:
                    self.chat_dict[chat_id].respond('List on position ' + str(number) + ' renamed as "' + new_name + '".')
                    return success
            if not success:
                success = self.db.rename_list_by_position(chat_id, number, new_name)
                if success:
                    self.chat_dict[chat_id].respond('List on position ' + str(number) + ' renamed as "' + new_name + '".')
                    return success
            if not success:
                self.chat_dict[chat_id].respond('Unknown list provided.')
            return success
        else:
            arguments = arguments.split('" "', 1)
            old_name = arguments[0][1:]
            new_name = arguments[0][:-1]
            list_id = self.db.get_list_id_by_name(chat_id, arguments[0][1:])
            if len(list_id) == 0:
                pass  # TODO

    def __populate_function_dictionary(self):
        self.add_function('/add.list', self.__add_list)
        self.add_function('/show.lists', self.__show_lists_of_lists)
        self.add_function('/delete.list', self.__delete_list)

