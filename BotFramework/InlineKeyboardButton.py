import sys


class InlineKeyboardButton:

    def __init__(self, text: str, url: str = None, callback_data: str = None, switch_inline_query: str = None,
                 switch_inline_query_current_chat: str = None, metadata: dict = None):
        assert url is None or isinstance(url, str)
        assert isinstance(text, str)
        assert callback_data is None or (isinstance(callback_data, str) and 1 <= sys.getsizeof(callback_data) <= 64)
        assert switch_inline_query is None or isinstance(switch_inline_query, str)
        assert switch_inline_query_current_chat is None or isinstance(switch_inline_query_current_chat, str)
        assert metadata is None or isinstance(metadata, dict)
        self.text = text
        self.url = url
        self.callback_data = callback_data
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.metadata = metadata

