import unittest
from BotFramework import Buttons, ReplyMarkups


class InlineKeyboardButtonsTest(unittest.TestCase):

    def test_ikb_create_with_text(self):

        ikb = Buttons.InlineKeyboardButton('name')

        self.assertEqual(ikb.get_text(), 'name')
        self.assertEqual(ikb.get_url(), None)
        self.assertEqual(ikb.get_callback_data(), None)
        self.assertEqual(ikb.get_switch_inline_query(), None)
        self.assertEqual(ikb.get_switch_inline_query_current_chat(), None)

    def test_ikb_create_with_text_url(self):

            ikb = Buttons.InlineKeyboardButton('name', 'www.google.com')

            self.assertEqual(ikb.get_text(), 'name')
            self.assertEqual(ikb.get_url(), 'www.google.com')
            self.assertEqual(ikb.get_callback_data(), None)
            self.assertEqual(ikb.get_switch_inline_query(), None)
            self.assertEqual(ikb.get_switch_inline_query_current_chat(), None)

    def test_ikb_create_with_text_url_callback(self):
        ikb = Buttons.InlineKeyboardButton('name', 'www.google.com', 'method-123-234')

        self.assertEqual(ikb.get_text(), 'name')
        self.assertEqual(ikb.get_url(), 'www.google.com')
        self.assertEqual(ikb.get_callback_data(), 'method-123-234')
        self.assertEqual(ikb.get_switch_inline_query(), None)
        self.assertEqual(ikb.get_switch_inline_query_current_chat(), None)

    def test_ikb_create_with_text_url_callback_switchiq(self):
        ikb = Buttons.InlineKeyboardButton('name', 'www.google.com', 'method-123-234', 'inline_query')

        self.assertEqual(ikb.get_text(), 'name')
        self.assertEqual(ikb.get_url(), 'www.google.com')
        self.assertEqual(ikb.get_callback_data(), 'method-123-234')
        self.assertEqual(ikb.get_switch_inline_query(), 'inline_query')
        self.assertEqual(ikb.get_switch_inline_query_current_chat(), None)

    def test_ikb_create_with_text_url_callback_switchiq_switchiqch(self):
        ikb = Buttons.InlineKeyboardButton('name', 'www.google.com', 'method-123-234', 'inline_query',
                                           'inline_query_current_chat')

        self.assertEqual(ikb.get_text(), 'name')
        self.assertEqual(ikb.get_url(), 'www.google.com')
        self.assertEqual(ikb.get_callback_data(), 'method-123-234')
        self.assertEqual(ikb.get_switch_inline_query(), 'inline_query')
        self.assertEqual(ikb.get_switch_inline_query_current_chat(), 'inline_query_current_chat')

    def test_ikb_create_with_incorrect_name(self):

        with self.assertRaises(AssertionError):
            Buttons.InlineKeyboardButton(1, 'www.google.com', 'method-123-234', 'inline_query',
                                            'inline_query_current_chat')

    def test_ikb_create_with_incorrect_callback(self):

        with self.assertRaises(AssertionError):
            Buttons.InlineKeyboardButton('ame', 'www.google.com', True, 'inline_query', 'inline_query_current_chat')

    def test_ikb_create_with_incorrect_url(self):

        with self.assertRaises(AssertionError):
            Buttons.InlineKeyboardButton('name', 1.98, 'method-123-234', 'inline_query', 'inline_query_current_chat')

    def test_ikb_create_with_incorrect_switchiq(self):

        with self.assertRaises(AssertionError):
            Buttons.InlineKeyboardButton('name', 'www.google.com', 'method-123-234', 9, 'inline_query_current_chat')

    def test_ikb_create_with_incorrect_switchiqch(self):

        with self.assertRaises(AssertionError):
            Buttons.InlineKeyboardButton('name', 'www.google.com', 'method-123-234', 'inline_query', 1)

    def test_ikb_create_with_too_big_callback(self):

        with self.assertRaises(AssertionError):
            Buttons.InlineKeyboardButton('name', url='www.google.com',
                                         callback_data=
                                         '12345678910111213141516171819202122232425262728293032333435363738',
                                         switch_inline_query='inline_query',
                                         switch_inline_query_current_chat='inline_query_current_chat')


class KeyboardButtonsTest(unittest.TestCase):

    def test_kb_create_with_text(self):

        kb = Buttons.KeyboardButton('name')

        self.assertEqual(kb.get_text(), 'name')
        self.assertEqual(kb.is_request_contact(), False)
        self.assertEqual(kb.is_request_location(), False)

    def test_kb_create_with_text_request_contact(self):

            kb = Buttons.KeyboardButton('name', request_contact=True)

            self.assertEqual(kb.get_text(), 'name')
            self.assertEqual(kb.is_request_contact(), True)
            self.assertEqual(kb.is_request_location(), False)

    def test_kb_create_with_text_request_location(self):

            kb = Buttons.KeyboardButton('name', request_location=True)

            self.assertEqual(kb.get_text(), 'name')
            self.assertEqual(kb.is_request_contact(), False)
            self.assertEqual(kb.is_request_location(), True)

    def test_kb_create_with_incorrect_name(self):

        with self.assertRaises(AssertionError):
            Buttons.KeyboardButton(1)

    def test_kb_create_with_incorrect_request_contact(self):

        with self.assertRaises(AssertionError):
            Buttons.KeyboardButton('name', request_contact=1)

    def test_kb_create_with_incorrect_request_location(self):

        with self.assertRaises(AssertionError):
            Buttons.KeyboardButton('name', request_location=1.0)


class InlineMarkupsTests(unittest.TestCase):

    def test_reply_keyboard_remove_get_reply_markup(self):
        rkr = ReplyMarkups.ReplyKeyboardRemove(True)
        self.assertEqual(rkr.get_markup(), {'selective': True, 'remove_keyboard': True})

    def test_ForceReply_get_reply_markup(self):
        fr = ReplyMarkups.ForceReply()
        self.assertEqual(fr.get_markup(), {'force_reply': True})

    def test_empty_ReplyKeyboardMarkup(self):
        rkm = ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
        self.assertEqual(rkm.get_markup(), {'resize_keyboard': True, 'keyboard': []})

    def test_ReplyKeyboardMarkup(self):
        rkm = ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add_button(Buttons.KeyboardButton('Text1', request_location=True), row=1, col=1)
        rkm.add_button(Buttons.KeyboardButton('Text2', True), row=2, col=1)
        self.assertEqual(str(rkm.get_markup()), "{'resize_keyboard': True, 'keyboard': [[{'text': 'Text1', " +
                                                "'request_location': True}], [{'text': 'Text2', 'request_contact': " +
                                                "True}]]}")

    def test_ReplyKeyboardMarkup_2cols(self):
        rkm = ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add_button(Buttons.KeyboardButton('Text1', request_location=True), row=1, col=1)
        rkm.add_button(Buttons.KeyboardButton('Text2', True), row=2, col=1)
        self.assertEqual(str(rkm.get_markup()), "{'resize_keyboard': True, 'keyboard': [[{'text': 'Text1', " +
                                                "'request_location': True}], [{'text': 'Text2', " +
                                                "'request_contact': True}]]}")

    def test_ReplyKeyboardMarkup_1row2cols(self):
        rkm = ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add_button(Buttons.KeyboardButton('Text1', request_location=True), row=1, col=1)
        rkm.add_button(Buttons.KeyboardButton('Text2', True), row=1, col=2)
        rkm.add_button(Buttons.KeyboardButton('Text3', True), row=2, col=2)
        self.assertEqual(str(rkm.get_markup()), "{'resize_keyboard': True, 'keyboard': [[{'text': 'Text1', " +
                                                "'request_location': True}, {'text': 'Text2', 'request_contact': True" +
                                                "}], [{'text': 'Text3', 'request_contact': True}]]}")

    def test_ReplyKeyboardMarkup_1row2cols(self):
        rkm = ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add_button(Buttons.KeyboardButton('Text1', request_location=True), row=1, col=1)
        rkm.add_button(Buttons.KeyboardButton('Text2', True), row=1, col=2)
        rkm.add_button(Buttons.KeyboardButton('Text3', True), row=2, col=1)
        self.assertEqual(str(rkm.get_markup()), "{'resize_keyboard': True, 'keyboard': [[{'text': 'Text1', " +
                                                "'request_location': True}, {'text': 'Text2', 'request_contact': " +
                                                "True}], [{'text': 'Text3', 'request_contact': True}]]}")

    def test_ReplyKeyboardMarkup_pop_button(self):
        rkm = ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add_button(Buttons.KeyboardButton('Text1', request_location=True), row=1, col=1)
        rkm.add_button(Buttons.KeyboardButton('Text2', True), row=1, col=2)
        rkm.add_button(Buttons.KeyboardButton('Text3', True), row=2, col=1)
        button = rkm.pop_button(row=1, col=1)
        self.assertEqual(str(button.get_markup()), "{'text': 'Text1', 'request_location': True}")
        self.assertEqual(str(rkm.get_markup()), "{'resize_keyboard': True, 'keyboard': [[{'text': 'Text2', " +
                                                "'request_contact': True}], [{'text': 'Text3', 'request_contact': " +
                                                "True}]]}")

    def test_ReplyKeyboardMarkup_move_button(self):
        rkm = ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
        rkm.add_button(Buttons.KeyboardButton('Text1', request_location=True), row=1, col=1)
        rkm.add_button(Buttons.KeyboardButton('Text2', True), row=1, col=2)
        rkm.add_button(Buttons.KeyboardButton('Text3', True), row=2, col=1)
        self.assertEqual(str(rkm.get_markup()), "{'resize_keyboard': True, 'keyboard': [[{'text': 'Text1', " +
                                                "'request_location': True}, {'text': 'Text2', 'request_contact': " +
                                                "True}], [{'text': 'Text3', 'request_contact': True}]]}")

    def test_ReplyKeyboardMarkup_1argError(self):
        with self.assertRaises(AssertionError):
            ReplyMarkups.ReplyKeyboardMarkup(resize_keyboard=1)

    def test_ReplyKeyboardMarkup_2argError(self):
        with self.assertRaises(AssertionError):
            ReplyMarkups.ReplyKeyboardMarkup(one_time_keyboard='True')

    def test_ReplyKeyboardMarkup_3argError(self):
        with self.assertRaises(AssertionError):
            ReplyMarkups.ReplyKeyboardMarkup(selective=1.0)

    def test_ReplyKeyboardMarkup_twice_the_same_place(self):
        with self.assertRaises(Exception):
            rkm = ReplyMarkups.ReplyKeyboardMarkup()
            rkm.add_button(Buttons.KeyboardButton('Text 1'), col=1, row=1)
            rkm.add_button(Buttons.KeyboardButton('Text 1'), col=1, row=1)

    def test_InlineKeyboardMarkup(self):
        ikm = ReplyMarkups.InlineKeyboardMarkup(resize_keyboard=False)
        ikm.add_button(Buttons.InlineKeyboardButton('Text1', callback_data='cbd'), row=1, col=1)
        ikm.add_button(Buttons.InlineKeyboardButton('Text2', switch_inline_query='switch_inline_query2'), row=1, col=2)
        ikm.add_button(Buttons.InlineKeyboardButton('Text3', switch_inline_query_current_chat=
                                                    'switch_inline_query_current_chat3'), row=1, col=3)
        button = ikm.pop_button(row=1, col=2)
        button.set_text('new text')
        ikm.add_button(button, row=2, col=1)
        ikm.add_button(Buttons.InlineKeyboardButton('Text1', callback_data='new button'), row=1, col=2)
        self.assertEqual(str(ikm.get_markup()), "{'inline_keyboard': [[{'text': 'Text1', 'callback_data': 'cbd'}, " +
                                                "{'text': 'Text1', 'callback_data': 'new button'}, {'text': 'Text3', " +
                                                "'switch_inline_query_current_chat': 'switch_inline_query_current_" +
                                                "chat3'}], [{'text': 'new text', 'switch_inline_query': " +
                                                "'switch_inline_query2'}]]}")

    def test_InlineKeyboardMarkup_wrong_button(self):
        with self.assertRaises(AssertionError):
            ikm = ReplyMarkups.InlineKeyboardMarkup()
            ikm.add_button('button', row=1, col=1)


if __name__ == '__main__':
    unittest.main()
