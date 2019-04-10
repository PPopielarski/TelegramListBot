

class Update():

    #  __slots__ = 'update_dict'

    def __init__(self, update: dict):
        self.update_dict = update
        self.chat_type = None
        self.is_edited = None
        self.is_forwarded = None
        self.is_callback = None
        self.media
        if 'message' in update:
            self.__is_callback_update = False
        elif 'callback_query' in update:
            self.__is_callback_update = True
        elif

    def is_channel_update(self):
        if 'channel_post' in self.update_dict or 'edited_channel_post' in self.update_dict:
            return True
        else:
            return False

    def is_private_update(self):
        if 'message' in self.update_dict and 'photo' in self.update_dict['message']['chat']['type'] == 'private':
            return True
        elif:


    def is_from_bot(self):
        if 'message' in self.update_dict:
            return True
        else:
            return False

    def contains_message(self):
        if 'message' in self.update_dict:
            return True
        else:
            return False

    def contains_command(self):
        if 'message' in self.update_dict and self.update_dict['message']['text'][0] == '/':
            return True
        else:
            return False

    def is_forward(self):
        if 'message' in self.update_dict and 'forward_from_chat' in self.update_dict['message']:
            return True
        else:
            return False
    
    def contains_photo(self):
        if 'message' in self.update_dict and 'photo' in self.update_dict['message']:
            return True
        else:
            return False
    

