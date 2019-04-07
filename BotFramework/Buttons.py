import sys


class _AbstractKeyboardButton:

    def __init__(self, text: str):
        assert isinstance(text, str), 'Argument text is not a string.'
        self.__text = text

    def set_text(self, text: str):
        assert isinstance(text, str), 'Argument text is not a string.'
        self.__text = text

    def get_text(self):
        return self.__text

    def get_markup(self):
        return {'text': self.__text}

    def get_markup_string(self):
        return str(self.get_markup())


class InlineKeyboardButton(_AbstractKeyboardButton):

    def __init__(self, text: str, url: str = None, callback_data: str = None, switch_inline_query: str = None,
                 switch_inline_query_current_chat: str = None):
        assert url is None or isinstance(url, str), 'Argument url is not a string.'
        assert callback_data is None or (isinstance(callback_data, str) and sys.getsizeof(callback_data) <= 64), \
            'Argument callback_data must be a string with size lower than 64 bytes or None type.'
        assert switch_inline_query is None or isinstance(switch_inline_query, str), \
            'Argument switch_inline_query is not a string.'
        assert switch_inline_query_current_chat is None or isinstance(switch_inline_query_current_chat, str), \
            'Argument switch_inline_query_current_chat is not a string.'
        _AbstractKeyboardButton.__init__(self, text)
        self.__url = url
        self.__callback_data = callback_data
        self.__switch_inline_query = switch_inline_query
        self.__switch_inline_query_current_chat = switch_inline_query_current_chat

    def get_url(self):
        return self.__url

    def set_url(self, url):
        assert url is None or isinstance(url, str), 'Argument url should be a string or None type.'
        self.__url = url

    def get_callback_data(self):
        return self.__callback_data

    def set_callback_data(self, callback_data):
        assert callback_data is None or (isinstance(callback_data, str) and sys.getsizeof(callback_data) <= 64), \
            'Argument callback_data must be a string with size lower than 64 bytes or None type.'
        self.__url = callback_data

    def get_switch_inline_query(self):
        return self.__switch_inline_query

    def set_switch_inline_query(self, switch_inline_query):
        assert switch_inline_query is None or isinstance(switch_inline_query, str), \
            'Argument switch_inline_query is not a string.'
        self.__switch_inline_query = switch_inline_query

    def get_switch_inline_query_current_chat(self):
        return self.__switch_inline_query_current_chat

    def set_switch_inline_query_current_chat(self, switch_inline_query_current_chat):
        assert switch_inline_query_current_chat is None or isinstance(switch_inline_query_current_chat, str), \
            'Argument switch_inline_query_current_chat is not a string.'
        self.__switch_inline_query_current_chat = switch_inline_query_current_chat

    def get_markup(self):
        d = super().get_markup()
        if self.__url:
            d['url'] = self.__url
        if self.__callback_data:
            d['callback_data'] = self.__callback_data
        if self.__switch_inline_query:
            d['switch_inline_query'] = self.__switch_inline_query
        if self.__switch_inline_query_current_chat:
            d['switch_inline_query_current_chat'] = self.__switch_inline_query_current_chat
        return d


class KeyboardButton(_AbstractKeyboardButton):

    def __init__(self, text: str, request_contact: bool = False, request_location: bool = False):
        _AbstractKeyboardButton.__init__(self, text)
        assert isinstance(request_contact, bool), 'Argument request_contact is not boolean.'
        assert isinstance(request_location, bool), 'Argument request_location is not boolean.'
        self.__request_contact = request_contact
        self.__request_location = request_location

    def is_request_contact(self):
        return self.__request_contact

    def set_request_contact(self, request_contact):
        assert isinstance(request_contact, bool), 'Argument request_contact is not boolean.'
        self.__request_contact = request_contact

    def is_request_location(self):
        return self.__request_location

    def set_request_location(self, request_location):
        assert isinstance(request_location, bool), 'Argument request_location is not boolean.'
        self.__request_location = request_location

    def get_markup(self):
        d = super().get_markup()
        if self.__request_contact:
            d['request_contact'] = self.__request_contact
        if self.__request_location:
            d['request_location'] = self.__request_location
        return d

