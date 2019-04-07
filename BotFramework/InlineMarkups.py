from BotFramework import Buttons


class _AbstractReplyMarkup(object):

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

    def get_markup_string(self):
        return str(self.get_markup())


class ReplyKeyboardRemove(_AbstractReplyMarkup):

    def __init__(self, selective: bool = False):
        _AbstractReplyMarkup.__init__(self, selective)

    def get_markup(self):
        d = super().get_markup()
        d['remove_keyboard'] = True
        return d


class ForceReply(_AbstractReplyMarkup):

    def __init__(self, selective: bool = False):
        _AbstractReplyMarkup.__init__(self, selective)

    def get_markup(self):
        d = super().get_markup()
        d['force_reply'] = True
        return d


class _KeyboardMarkup(_AbstractReplyMarkup):

    __slots__ = '__resize_keyboard', '__one_time_keyboard', '_rows_dict'

    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = False, selective: bool = False):
        assert isinstance(resize_keyboard, bool), 'Argument resize_keyboard must be boolean type.'
        assert isinstance(one_time_keyboard, bool), 'Argument resize_keyboard must be boolean type.'
        assert isinstance(selective, bool), 'Argument resize_keyboard must be boolean type.'
        _AbstractReplyMarkup.__init__(self, selective)
        self.__resize_keyboard = resize_keyboard
        self.__one_time_keyboard = one_time_keyboard
        self._rows_dict = {}

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

    def get_keyboard_list(self):
        buttons_list_of_lists = []
        for row_number in sorted(self._rows_dict):
            buttons_list = []
            for col_number in sorted(self._rows_dict[row_number]):
                buttons_list.append(self._rows_dict[row_number][col_number].get_as_string())
            buttons_list_of_lists.append(buttons_list)
        return buttons_list_of_lists

    def add_button(self, button, row: int = None, column: int = None):
        assert row is None or isinstance(row, int), 'Argument row must be int or None type'
        assert column is None or isinstance(column, int), 'Argument column must be int or None type'

        if row is None:
            if len(self._rows_dict) == 0:
                row = 0
            else:
                row = max(self._rows_dict) + 1

        if row not in self._rows_dict:
            self._rows_dict[row] = {}
        elif column in self._rows_dict[row]:
            raise Exception('''Button in this position is already set. Use pop_button to remove it or change its 
                            position.''')

        if column is None:
            if len(self._rows_dict[row]) == 0:
                column = 0
            else:
                column = max(self._rows_dict[row]) + 1

        if column in self._rows_dict[row]:
            raise Exception(
                'Button in this position is already set. Use pop_button to remove it or change coordinates.')

        self._rows_dict[row][column] = button

    def pop_buttons(self, row: int = None, column: int = None):
        """Removes and returns button from position. Returns none if there was no button on specified position.
        If column or row is not specified it returns list of buttons from row or column."""
        if row is not None and column is not None:
            if row in self._rows_dict and column in self._rows_dict[row]:
                return self._rows_dict[row].pop(column)
            else:
                return None
        elif row in self._rows_dict:
            return self._rows_dict.pop(row)
        else:
            col = {}
            for i in self._rows_dict:
                col[i] = self._rows_dict.pop(column)

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

    def add_button(self, button: Buttons.InlineKeyboardButton, row: int = None, column: int = None):
        assert isinstance(button, Buttons.InlineKeyboardButton), 'Argument button must be InlineKeyboardButton.'
        super().add_button(button, row, column)

    def get_markup(self):
        d = super().get_markup()
        d['inline_keyboard'] = super().get_keyboard_list()
        return d


class ReplyKeyboardMarkup(_KeyboardMarkup):

    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = False, selective: bool = False):
        _KeyboardMarkup.__init__(self, resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard,
                                 selective=selective)

    def add_button(self, button: Buttons.KeyboardButton, row: int = None, column: int = None):
        assert isinstance(button, Buttons.KeyboardButton), 'Argument button must be KeyboardButton.'
        super().add_button(button, row, column)

    def get_markup(self):
        d = super().get_markup()
        d['keyboard'] = super().get_keyboard_list()
        return d
