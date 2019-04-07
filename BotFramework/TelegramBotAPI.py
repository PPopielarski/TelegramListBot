import json
import requests
from BotFramework import ReplyMarkups


class TelegramBotAPI:

    __slots__ = '__url'

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

    def send_message(self, chat_id, text: str, parse_mode: str = None, disable_web_page_preview: bool = False,
                     disable_notification: bool = False, reply_to_message_id: int = None, reply_markup=None):
        if issubclass(type(reply_markup), ReplyMarkups._KeyboardMarkup):
            reply_markup = reply_markup.get_markup()
        request = {"method": "sendMessage", "text": text, "chat_id": chat_id}
        if disable_web_page_preview:
            request['disable_web_page_preview'] = disable_web_page_preview
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        if parse_mode:
            request['parse_mode'] = parse_mode
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
        request = {"method": "editMessageText", "text": new_text, "chat_id": chat_id, 'message_id': message_id}
        if new_reply_markup:
            request['reply_markup'] = new_reply_markup
        return self.__send_post_request(request)

    def delete_message(self, chat_id, message_id):
        return self.__send_post_request({"method": "deleteMessage",  "chat_id": chat_id, 'message_id': message_id})

    def send_photo(self, chat_id, photo, caption=None, parse_mode=None, disable_notification=False,
                   reply_to_message_id=None, reply_markup=None):
        request = {"method": "sendPhoto", 'chat_id': chat_id, 'photo': photo}
        if caption:
            request['caption'] = caption
        if parse_mode:
            request['parse_mode'] = parse_mode
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def send_audio(self, chat_id, audio, caption=None, parse_mode=None, duration=None, performer=None, title=None,
                   thumb=None, disable_notification=False, reply_to_message_id=None, reply_markup=None):
        request = {"method": "sendAudio", 'chat_id': chat_id, 'audio': audio}
        if caption:
            request['caption'] = caption
        if parse_mode:
            request['parse_mode'] = parse_mode
        if duration:
            request['duration'] = duration
        if performer:
            request['performer'] = performer
        if title:
            request['title'] = title
        if thumb:
            request['thumb'] = thumb
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def send_document(self, chat_id, document, thumb=None, caption=None, parse_mode=None, disable_notification=False,
                      reply_to_message_id=None, reply_markup=None):
        request = {"method": "sendDocument", 'chat_id': chat_id, 'document': document}
        if thumb:
            request['thumb'] = thumb
        if caption:
            request['caption'] = caption
        if parse_mode:
            request['parse_mode'] = parse_mode
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def send_video(self, chat_id, video, thumb=None, caption=None, parse_mode=None, disable_notification=False,
                   reply_to_message_id=None, reply_markup=None):
        request = {"method": "sendVideo", 'chat_id': chat_id, 'video': video}
        if thumb:
            request['thumb'] = thumb
        if caption:
            request['caption'] = caption
        if parse_mode:
            request['parse_mode'] = parse_mode
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)
