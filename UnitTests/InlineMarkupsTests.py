import unittest
from BotFramework import Buttons, InlineMarkups


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

    def test_reply_keyboard_remove(self):
        rkr = InlineMarkups.ReplyKeyboardRemove()
        self.assertEqual(rkr.get_markup(), {'remove_keyboard': True})

    def test_reply_keyboard_remove_get_reply_markup(self):
        rkr = InlineMarkups.ReplyKeyboardRemove(True)
        self.assertEqual(rkr.get_markup_string(), str({'selective': True, 'remove_keyboard': True}))

    def test_ForceReply(self):
        fr = InlineMarkups.ForceReply(True)
        self.assertEqual(fr.get_markup(), {'force_reply': True, 'selective': True})

    def test_ForceReply_get_reply_markup(self):
        fr = InlineMarkups.ForceReply()
        self.assertEqual(fr.get_markup_string(), str({'force_reply': True}))

    def test_empty_ReplyKeyboardMarkup(self):
        rkm = InlineMarkups.ReplyKeyboardMarkup(resize_keyboard=True)
        self.assertEqual(rkm.get_markup_string(), str({'resize_keyboard': True, 'keyboard': []}))


if __name__ == '__main__':
    unittest.main()
