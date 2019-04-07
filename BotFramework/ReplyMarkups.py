from BotFramework import Buttons


class _ReplyMarkup(object):

    __slots__ = '__selective'

    def __init__(self, selective):
        assert isinstance(selective, bool), 'Argument selective must be boolean type.'
        self.__selective = selective

    def set_selective(self, value: bool):
        assert isinstance(value, bool)
        self.__selective = {'selective': value}

    def is_selective(self):
        return self.__selective

    def get_markup(self):
        if self.__selective:
            return {'selective': True}
        else:
            return {}


class ReplyKeyboardRemove(_ReplyMarkup):

    def __init__(self, selective: bool = False):
        _ReplyMarkup.__init__(self, selective)

    def get_markup(self):
        d = super().get_markup()
        d['remove_keyboard'] = True
        return d


class ForceReply(_ReplyMarkup):

    def __init__(self, selective: bool = False):
        _ReplyMarkup.__init__(self, selective)

    def get_markup(self):
        d = super().get_markup()
        d['force_reply'] = True
        return d


class _KeyboardMarkup(_ReplyMarkup):

    __slots__ = '__resize_keyboard', '__one_time_keyboard', '__rows_dict'

    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = False, selective: bool = False):
        assert isinstance(resize_keyboard, bool), 'Argument resize_keyboard must be boolean type.'
        assert isinstance(one_time_keyboard, bool), 'Argument resize_keyboard must be boolean type.'
        assert isinstance(selective, bool), 'Argument resize_keyboard must be boolean type.'
        _ReplyMarkup.__init__(self, selective)
        self.__resize_keyboard = resize_keyboard
        self.__one_time_keyboard = one_time_keyboard
        self.__rows_dict = {}

    def set_resize_keyboard(self, value: bool):
        assert isinstance(value, bool), 'Argument value must be boolean type.'
        self.__resize_keyboard = value

    def is_resize_keyboard(self):
        return self.__resize_keyboard

    def set_one_time_keyboard(self, value: bool):
        assert isinstance(value, bool), 'Argument value must be boolean type.'
        self.__one_time_keyboard = value

    def is_one_time_keyboard(self):
        return self.__one_time_keyboard

    def _get_keyboard_list(self):
        buttons_list_of_lists = []
        for row_number in sorted(self.__rows_dict):
            buttons_list = []
            for col_number in sorted(self.__rows_dict[row_number]):
                buttons_list.append(self.__rows_dict[row_number][col_number].get_markup())
            buttons_list_of_lists.append(buttons_list)
        return buttons_list_of_lists

    def add_button(self, button, row: int, col: int):
        assert isinstance(row, int), 'Argument row must be int.'
        assert isinstance(col, int), 'Argument col must be int.'
        if row not in self.__rows_dict:
            self.__rows_dict[row] = {}
        elif col in self.__rows_dict[row]:
            raise Exception('''Button in this position is already set. Use pop_button to remove it or change its 
                            position.''')
        self.__rows_dict[row][col] = button

    def pop_button(self, row: int, col: int):
        """Removes and returns button from position. Returns None if there was no button on specified position."""
        if row in self.__rows_dict and col in self.__rows_dict[row]:
            button = self.__rows_dict[row].pop(col)
            if len(self.__rows_dict[row]) == 0:
                self.__rows_dict.pop(row)
            return button
        else:
            return None

    def move_button(self, row: int, col: int, new_row: int, new_col: int):
        if new_row in self.__rows_dict and new_col in self.__rows_dict[row]:
            raise Exception('Button at this position is already set.')
        if row not in self.__rows_dict or col not in self.__rows_dict[row]:
            raise Exception("Button does not not exist.")
        if new_row not in self.__rows_dict:
            self.__rows_dict[new_row] = {}
        self.__rows_dict[new_row][new_col] = self.pop_button(row, col)

    def get_markup(self):
        d = super().get_markup()
        if self.__resize_keyboard:
            d['resize_keyboard'] = True
        if self.__one_time_keyboard:
            d['one_time_keyboard'] = True
        return d


class InlineKeyboardMarkup(_KeyboardMarkup):

    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = False, selective: bool = False):
        _KeyboardMarkup.__init__(self, resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard,
                                 selective=selective)

    def add_button(self, button: Buttons.InlineKeyboardButton, row: int = None, col: int = None):
        assert isinstance(button, Buttons.InlineKeyboardButton), 'Argument button must be InlineKeyboardButton.'
        super().add_button(button, row, col)

    def get_markup(self):
        d = super().get_markup()
        d['inline_keyboard'] = super()._get_keyboard_list()
        return d


class ReplyKeyboardMarkup(_KeyboardMarkup):

    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = False, selective: bool = False):
        _KeyboardMarkup.__init__(self, resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard,
                                 selective=selective)

    def add_button(self, button: Buttons.KeyboardButton, row: int = None, col: int = None):
        assert isinstance(button, Buttons.KeyboardButton), 'Argument button must be KeyboardButton.'
        super().add_button(button, row, col)

    def get_markup(self):
        d = super().get_markup()
        d['keyboard'] = super()._get_keyboard_list()
        return d
