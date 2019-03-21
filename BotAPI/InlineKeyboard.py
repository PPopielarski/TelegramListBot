
class InlineKeyboard:

    def __init__(self):
        self.row_dict = {}
        self.max_row = 0
        self.keyboard_string = None

    def __add_to_dictionary(self, button_text, row, column):
        if row in self.row_dict:
            self.row_dict[row][column] = button_text
        else:
            self.row_dict[row] = {}
            self.row_dict[row][column] = button_text

    def add_button(self, text, callback_data, row=None, column=None, url=None):
        if row is None:
            self.max_row = self.max_row + 1
            row = self.max_row
        elif self.max_row < row:
            self.max_row = row
        if column is None:
            column = 1
        button_text = '{"text":"' + text + '","callback_data":"' + callback_data + (',"url":"' + url + '"' if url else '') + '"}'
        self.__add_to_dictionary(button_text, row, column)

    def delete_button(self, row, column):
        self.button_dict.pop((row, column), None)

    def refresh_keyboard_string(self):
        s = "["
        for row in sorted(self.row_dict):
            row_text = "["
            for col in sorted(self.row_dict[row]):
                row_text = row_text + self.row_dict[row][col] + ","
            s = s + row_text[:-1]+"],"
        self.keyboard_string = s[:-1] + "]"

