from BotFramework import InlineKeyboardButton
import sys

# TODO adjust class for saving into database as a operation for whole keyboard (destructor of the class or method for
# TODO changing current view of chat)


class InlineKeyboard:

    @classmethod
    def from_json(cls, json_data):
        resize_keyboard = json_data['resize_keyboard'] if 'resize_keyboard' in json_data else False
        one_time_keyboard = json_data['one_time_keyboard'] if 'one_time_keyboard' in json_data else False
        selective = json_data['selective'] if 'selective' in json_data else False
        rows_dict = {}
        if 'inline_keyboard' in json_data:
            buttons_list_of_lists = json_data['inline_keyboard']
            for list_number in range(len(buttons_list_of_lists)):
                rows_dict[list_number] = {}
                for button_number in range(len(buttons_list_of_lists[list_number])):
                    rows_dict[list_number][button_number] = buttons_list_of_lists[list_number][button_number]
        ik = InlineKeyboard(resize_keyboard, one_time_keyboard, selective)
        ik.__rows_dict = rows_dict
        return ik

    def __init__(self, resize_keyboard=True, one_time_keyboard=True, selective=False):
        self.__rows_dict = {}
        self.resize_keyboard = resize_keyboard
        self.selective = selective
        self.one_time_keyboard = one_time_keyboard

    def __str__(self):
        return self.get_keyboard_markup()

    def add_button(self, button: InlineKeyboardButton.InlineKeyboardButton, row: int = None, column: int = None):
        assert isinstance(button, InlineKeyboardButton.InlineKeyboardButton)
        assert row is None or isinstance(row, int)
        assert column is None or isinstance(column, int)
        if row is None:
            if len(self.__rows_dict) == 0:
                row = 0
            else:
                row = max(self.__rows_dict) + 1

        if row not in self.__rows_dict:
            self.__rows_dict[row] = {}
        elif column in self.__rows_dict[row]:
            raise Exception('''Button in this position is already set. Use pop_button to remove it or change its 
                            position.''')

        if column is None:
            if len(self.__rows_dict[row]):
                column = 0
            else:
                column = max(self.__rows_dict[row]) + 1

        if column in self.__rows_dict[row]:
            raise Exception(
                'Button in this position is already set. Use pop_button to remove it or change coordinates.')


    def create_button(self, text: str, url: str = None, callback_data: str = None, switch_inline_query: str = None,
                      switch_inline_query_current_chat: str = None, metadata: dict = None, row=None, column=None):
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
            raise Exception(
                'Button in this position is already set. Use pop_button to remove it or change coordinates.')

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

    def move_button(self, current_position_row, current_position_column,
                    offset_row=None, offset_column=None, new_row=None, new_column=None):
        if current_position_row in self.__rows_dict:
            if current_position_column not in self.__rows_dict[current_position_row]:
                raise Exception('No button on such position.')
        else:
            raise Exception('No button on such position.')

        if offset_row is not None and new_row is None:
            new_row = current_position_row + offset_row
        elif offset_row is None and new_row is None:
            raise Exception('Incorrect specification of new button position.')

        if offset_column is not None and new_column is None:
            new_column = current_position_column + offset_column
        elif offset_column is None and new_column is None:
            raise Exception('Incorrect specification of new button column.')

        if new_row not in self.__rows_dict:
            self.__rows_dict[new_row] = {}

        self.__rows_dict[new_row][new_column] = self.__rows_dict[current_position_row].pop(current_position_column)

    def get_keyboard_markup(self):
        buttons_list_of_lists = []
        for row_number in sorted(self.__rows_dict):
            buttons_list = []
            for col_number in sorted(self.__rows_dict[row_number]):
                buttons_list.append(self.__rows_dict[row_number][col_number])
            buttons_list_of_lists.append(buttons_list)
        return {'resize_keyboard': self.resize_keyboard, 'one_time_keyboard': self.one_time_keyboard,
                'selective': self.selective, 'inline_keyboard': buttons_list_of_lists}