import sys
import operator


class InlineKeyboard:

    def __init__(self, resize_keyboard=True, one_time_keyboard=False):
        self.__rows_dict = {}
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

    def add_button(self, text, callback_data, row=None, column=None, url=None):
        """Indexes of rows and columns can contain gaps (e.g. 1, 2, 4) and start from any value."""
        if sys.getsizeof(callback_data) > 64:
            raise Exception('Callback data maximum weight is 64.')

        if row is None:
            if len(self.__rows_dict) == 0:
                row = 0
            else:
                row = max(self.__rows_dict) + 1

        if row not in self.__rows_dict:
            self.__rows_dict[row] = {}
        elif column in self.__rows_dict[row]:
            raise Exception('Button in this position is already set. ' +
                            'Use pop_button to remove it or change coordinates.')

        if column is None:
            if len(self.__rows_dict):
                column = 0
            else:
                column = max(self.__rows_dict[row]) + 1
        if column in self.__rows_dict[row]:
            raise Exception('Button in this position is already set. Use pop_button to remove it or change coordinates.')

        button = {"text": text, "callback_data": callback_data}
        if url:
            button["url"] = url
        self.__rows_dict[row][column] = button

    def pop_button(self, row, column):
        """Removes and returns button from position. Returns none if there was no button on specified position."""
        if row in self.__rows_dict:
            if column in self.__rows_dict[row]:
                return self.__rows_dict[row].pop(column)
            else:
                return None
        else:
            return None

    def get_keyboard_markup(self):
        buttons_list_of_lists = []
        for row_number in sorted(self.__rows_dict):
            buttons_list = []
            for col_number in sorted(self.__rows_dict[row_number]):
                buttons_list.append(self.__rows_dict[row_number][col_number])
            buttons_list_of_lists.append(buttons_list)

        return {'resize_keyboard': self.resize_keyboard, 'one_time_keyboard': self.one_time_keyboard,
                'inline_keyboard': buttons_list_of_lists}
