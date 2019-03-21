
class InlineKeyboard:

    def __init__(self):
        self.row_dict = {}
        self.max_row = 0
        self.keyboard_string = None

    def add_button(self, text, callback_data, row=None, column=None, url=None):
        if row is None:
            row = max(self.row_dict)+1
        if column is None:
            column = 1
        button_text = '{"text":"' + text + '","callback_data":"' + callback_data + \
                      (',"url":"' + url + '"' if url else '') + '"}'
        if row in self.row_dict:
            self.row_dict[row][column] = button_text
        else:
            self.row_dict[row] = {}
            self.row_dict[row][column] = button_text

    def delete_button(self, row, column):
        self.row_dict[row].pop(column, None)
        if len(self.row_dict[row]) == 0:
            self.row_dict.pop(row, None)

    def refresh_keyboard_string(self):
        s = "["
        for row in sorted(self.row_dict):
            row_text = "["
            for col in sorted(self.row_dict[row]):
                row_text = row_text + self.row_dict[row][col] + ","
            s = s + row_text[:-1]+"],"
        self.keyboard_string = s[:-1] + "]"

    def get_keyboard_string(self):
        return self.keyboard_string
