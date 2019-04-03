import json
import requests


class TelegramBotAPI:

    def __init__(self, token):
        self.__url = 'https://api.telegram.org/bot' + token + '/'

    def __send_post_request(self, parameters_dict):
        """Sends request to bot and returns json file with response
        Args: parameters_dict is a dictionary with parameters"""
        return json.loads(requests.post(self.__url, json=parameters_dict).content.decode("utf8"))

    def get_bot_details(self):
        return self.__send_post_request({"method": "getme"})

    def get_updates(self, offset, timeout=100):
        return self.__send_post_request({"offset": offset, "timeout": timeout, "method": "getUpdates"})

    def send_message(self, text, chat_id, reply_markup=None):
        if reply_markup is not None and type(reply_markup) is not str:
            reply_markup = reply_markup.get_keyboard_markup()
        request = {"method": "sendMessage", "text": text, "chat_id": chat_id}
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def send_chat_action(self, chat_id, action):
        """Possible actions: 'typing', 'upload_photo', 'upload_video', 'record_video', 'upload_audio', 'record_audio',
                          'upload_document', 'find_location', 'upload_video_note', 'record_video_note'"""
        return self.__send_post_request({"method": "sendChatAction", "action": action, "chat_id": chat_id})

    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=False):
        request = {"method": "forwardMessage", "from_chat_id": from_chat_id, "chat_id": chat_id,
                   'message_id': message_id}
        if disable_notification:
            request['disable_notification'] = True
        return self.__send_post_request(request)

    def edit_message(self, new_text, chat_id, message_id, new_reply_markup=None):
        request = {"method": "editMessageText", "text": new_text, "chat_id": chat_id,
                   'message_id': message_id}
        if new_reply_markup:
            request['reply_markup'] = new_reply_markup
        return self.__send_post_request(request)

    def delete_message(self, chat_id, message_id):
        return self.__send_post_request({"method": "deleteMessage",  "chat_id": chat_id, 'message_id': message_id})
