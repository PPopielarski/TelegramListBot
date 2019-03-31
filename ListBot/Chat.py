from BotAPI import InlineKeyboard


class Chat:

    """
    Callback query pattern: action_name-list_id-item_id
    Possible action names:
        show_list-list_id
        add_list

    Possible chat states:
    0 - view list of lists
    1-list_id - view of list items
    """

    def __init__(self, chat_id, bot_api):
        self.bot_api = bot_api
        self.chat_id = chat_id
        self.last_message_id = None
        self.state = None
        self.command = None

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

    """def handle_command(self, command):
        # SHOW LIST
        elif len(strip) >= 10 and strip[:10] is '/show_list':
            strip = strip[10:].strip()
            if len(strip) == 0 or (len(strip) == 2 and strip[0] == '"' and strip[1] == '"'):
                self.__respond(text="Enter list number, name or ID.\n
                If list name contains only digits enter it in quotation marks.\n
                If list name is surrounded by question marks enter them twice e.g. ""name"".                
                ", force_message=True)
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

        Used in or to reach state 0, when the user see list of list.
        



"""