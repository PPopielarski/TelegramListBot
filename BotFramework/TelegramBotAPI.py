import json
import requests
from BotFramework import ReplyMarkups


#  TODO handle chat_id - it can be int or string


class TelegramBotAPI:

    __slots__ = '__url'

    def __init__(self, token):
        self.__url = 'https://api.telegram.org/bot' + token + '/'

    def __send_post_request(self, parameters_dict):
        """Sends request to bot and returns json file with response
        Args: parameters_dict is a dictionary with parameters"""
        return json.loads(requests.post(self.__url, json=parameters_dict).content.decode("utf8"))

    def get_me(self) -> dict:
        return self.__send_post_request({"method": "getme"})

    def get_updates(self, offset: int = None, timeout: int = 100) -> dict:
        assert offset is None or isinstance(offset, int)
        assert isinstance(timeout, int)
        return self.__send_post_request({"offset": offset, "timeout": timeout, "method": "getUpdates"})

    def send_message(self, chat_id, text: str, parse_mode: str = None, disable_web_page_preview: bool = False,
                     disable_notification: bool = False, reply_to_message_id: int = None, reply_markup=None) -> dict:
        if issubclass(type(reply_markup), ReplyMarkups._ReplyMarkup):
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

    def send_chat_action(self, chat_id, action: str) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        assert action in ('typing', 'upload_photo', 'record_video', 'upload_video', 'record_audio', 'upload_audio',
                          'upload_document', 'find_location', 'record_video_note', 'upload_video_note')
        return self.__send_post_request({"method": "sendChatAction", "action": action, "chat_id": chat_id})

    def forward_message(self, chat_id, from_chat_id, message_id: int, disable_notification: bool = False) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        assert isinstance(from_chat_id, int) or (isinstance(from_chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        assert isinstance(message_id, int)
        assert isinstance(disable_notification, bool)
        request = {"method": "forwardMessage", "from_chat_id": from_chat_id, "chat_id": chat_id,
                   'message_id': message_id}
        if disable_notification:
            request['disable_notification'] = True
        return self.__send_post_request(request)

    def edit_message_text(self, chat_id, message_id: int, new_text: str,
                          parse_mode: str = None, disable_web_page_preview: bool = False,
                          new_reply_markup: ReplyMarkups.InlineKeyboardMarkup = None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        assert isinstance(message_id, int)
        assert isinstance(new_text, str)
        assert parse_mode is None or isinstance(parse_mode, str)
        assert isinstance(disable_web_page_preview, bool)
        assert new_reply_markup is None or isinstance(new_reply_markup, ReplyMarkups.InlineKeyboardMarkup)
        request = {"method": "editMessageText", "text": new_text, "chat_id": chat_id, 'message_id': message_id}
        if new_reply_markup:
            request['reply_markup'] = new_reply_markup
        if parse_mode:
            request['parse_mode'] = parse_mode
        if disable_web_page_preview:
            request['disable_web_page_preview'] = True
        return self.__send_post_request(request)

    def edit_message_text_inline(self, new_text: str, inline_message_id: str, parse_mode: str = None,
                                 disable_web_page_preview: bool = False,
                                 new_reply_markup: ReplyMarkups.InlineKeyboardMarkup = None) -> dict:
        assert isinstance(inline_message_id, str)
        assert isinstance(new_text, str)
        assert isinstance(parse_mode, str) or parse_mode is None
        assert isinstance(disable_web_page_preview, bool)
        assert isinstance(new_reply_markup, ReplyMarkups.InlineKeyboardMarkup) or new_reply_markup is None
        request = {"method": "editMessageText", "text": new_text, "inline_message_id": inline_message_id}
        if new_reply_markup:
            request['reply_markup'] = new_reply_markup
        if parse_mode:
            request['parse_mode'] = parse_mode
        if disable_web_page_preview:
            request['disable_web_page_preview'] = True
        return self.__send_post_request(request)

    def edit_message_caption(self, chat_id, message_id: int, new_caption: str,
                             parse_mode: str = None,
                             new_reply_markup: ReplyMarkups.InlineKeyboardMarkup = None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        assert isinstance(message_id, int)
        assert isinstance(new_caption, str)
        assert parse_mode is None or isinstance(parse_mode, str)
        assert isinstance(new_reply_markup, ReplyMarkups.InlineKeyboardMarkup) or new_reply_markup is None
        request = {"method": "editMessageCaption", "caption": new_caption, "chat_id": chat_id, 'message_id': message_id}
        if new_reply_markup:
            request['reply_markup'] = new_reply_markup
        if parse_mode:
            request['parse_mode'] = parse_mode
        return self.__send_post_request(request)

    def edit_message_caption_inline(self, new_caption: str, inline_message_id: str, parse_mode: str = None,
                                    new_reply_markup: ReplyMarkups.InlineKeyboardMarkup = None) -> dict:
        assert isinstance(inline_message_id, str)
        assert isinstance(new_caption, str)
        assert isinstance(parse_mode, str) or parse_mode is None
        assert isinstance(new_reply_markup, ReplyMarkups.InlineKeyboardMarkup) or new_reply_markup is None
        request = {"method": "editMessageCaption", "caption": new_caption, "inline_message_id": inline_message_id}
        if new_reply_markup:
            request['reply_markup'] = new_reply_markup
        if parse_mode:
            request['parse_mode'] = parse_mode
        return self.__send_post_request(request)

    def edit_message_reply_markup(self, chat_id, message_id: int,
                                  new_reply_markup: ReplyMarkups._ReplyMarkup = None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        assert isinstance(message_id, int)
        assert issubclass(type(new_reply_markup), ReplyMarkups._ReplyMarkup) or new_reply_markup is None
        request = {"method": "editMessageReplyMarkup", "chat_id": chat_id, 'message_id': message_id}
        if new_reply_markup:
            request['reply_markup'] = new_reply_markup
        return self.__send_post_request(request)

    def edit_message_reply_markup_inline(self, inline_message_id: str,
                                         new_reply_markup: ReplyMarkups._ReplyMarkup = None) -> dict:
        assert isinstance(inline_message_id, str)
        assert issubclass(type(new_reply_markup), ReplyMarkups._ReplyMarkup) or new_reply_markup is None
        request = {"method": "editMessageReplyMarkup"}
        if new_reply_markup:
            request['reply_markup'] = new_reply_markup
        return self.__send_post_request(request)

    def delete_message(self, chat_id, message_id: int) -> dict:
        assert isinstance(message_id, int)
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "deleteMessage",  "chat_id": chat_id, 'message_id': message_id})

    # TODO input file handling - photo
    def send_photo(self, chat_id, photo, caption: str = None, parse_mode: str = None,
                   disable_notification: bool = False,  reply_to_message_id: int = None,
                   reply_markup: ReplyMarkups._ReplyMarkup = None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        assert isinstance(caption, str) or caption is None
        assert isinstance(parse_mode, str) or parse_mode is None
        assert isinstance(disable_notification, bool)
        assert isinstance(reply_to_message_id, int) or reply_to_message_id is None
        assert issubclass(type(reply_markup), ReplyMarkups._ReplyMarkup) or reply_markup is None
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

    # TODO input file handling - audio, thumb
    def send_audio(self, chat_id, audio, caption: str = None, parse_mode: str = None, duration: int = None,
                   performer: str = None, title: str = None, thumb=None, disable_notification: bool = False,
                   reply_to_message_id: int = None, reply_markup: ReplyMarkups._ReplyMarkup = None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        assert caption is None or (isinstance(caption, str) and len(caption) <= 1024)
        assert parse_mode is None or isinstance(parse_mode, str)
        assert duration is None or isinstance(duration, int)
        assert performer is None or isinstance(performer, str)
        assert title is None or isinstance(title, str)
        assert isinstance(disable_notification, bool)
        assert reply_to_message_id is None or isinstance(reply_to_message_id, int)
        assert reply_markup is None or issubclass(type(reply_markup), ReplyMarkups._ReplyMarkup)
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

    def send_document(self, chat_id, document, thumb=None, caption=None, parse_mode=None,
                      disable_notification: bool = False, reply_to_message_id=None, reply_markup=None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
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

    def send_video(self, chat_id, video, thumb=None, caption=None, parse_mode=None, disable_notification: bool = False,
                   reply_to_message_id=None, reply_markup=None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
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

    def send_animation(self, chat_id, animation, duration: int = None, width: int = None, height: int = None,
                       thumb=None, caption=None, parse_mode=None, disable_notification: bool = False,
                       reply_to_message_id: int = None, reply_markup=None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        request = {"method": "sendAnimation", 'chat_id': chat_id, 'animation': animation}
        if duration:
            request['duration'] = duration
        if width:
            request['width'] = width
        if height:
            request['height'] = height
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

    def send_voice(self, chat_id, voice, duration: int = None, caption=None, parse_mode=None,
                   disable_notification: bool = False, reply_to_message_id: int = None, reply_markup=None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        request = {"method": "sendVoice", 'chat_id': chat_id, 'voice': voice}
        if duration:
            request['duration'] = duration
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

    def send_video_note(self, chat_id: int, video_note, duration: int = None, length: int =None, thumb=None,
                        disable_notification: bool = False, reply_to_message_id: int = None, reply_markup=None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        request = {"method": "sendVideoNote", 'chat_id': chat_id, 'video_note': video_note}
        if duration:
            request['duration'] = duration
        if length:
            request['length'] = length
        if thumb:
            request['thumb'] = thumb
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def send_media_group(self, chat_id, media, disable_notification: bool = False,  # TODO obiekty do media
                         reply_to_message_id: int = None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        request = {"method": "sendMediaGroup", 'chat_id': chat_id, 'media': media}
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        return self.__send_post_request(request)

    def send_location(self, chat_id, latitude: int, longitude: int, live_period: int = None,
                      disable_notification: bool = False, reply_to_message_id: int = None, reply_markup=None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        request = {"method": "sendLocation", 'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
        if live_period:
            request['live_period'] = live_period
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def edit_message_live_location_inline(self, inline_message_id: str, latitude: float, longitude: float,
                                          reply_markup: ReplyMarkups.InlineKeyboardMarkup = None) -> dict:
        assert isinstance(inline_message_id, str)
        assert isinstance(latitude, float)
        assert isinstance(longitude, float)
        assert isinstance(reply_markup, ReplyMarkups.InlineKeyboardMarkup)
        request = {"method": "editMessageLiveLocation", 'inline_message_id': inline_message_id, 'latitude': latitude,
                   'longitude': longitude}
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def edit_message_live_location(self, chat_id, message_id: int, latitude: float, longitude: float,
                                   reply_markup: ReplyMarkups.InlineKeyboardMarkup = None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        assert isinstance(message_id, int)
        assert isinstance(latitude, float)
        assert isinstance(longitude, float)
        assert isinstance(reply_markup, ReplyMarkups.InlineKeyboardMarkup) or reply_markup is None
        request = {"method": "editMessageLiveLocation", 'chat_id': chat_id, 'latitude': latitude,
                   'longitude': longitude, 'message_id': message_id}
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def stop_message_live_location_inline(self, inline_message_id: str,
                                          reply_markup: ReplyMarkups.InlineKeyboardMarkup = None) -> dict:
        assert isinstance(inline_message_id, str)
        assert isinstance(reply_markup, ReplyMarkups.InlineKeyboardMarkup)
        request = {"method": "stopMessageLiveLocation", 'inline_message_id': inline_message_id}
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def stop_message_live_location(self, chat_id, message_id: int,
                                   reply_markup: ReplyMarkups.InlineKeyboardMarkup = None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        assert isinstance(message_id, int)
        assert isinstance(reply_markup, ReplyMarkups.InlineKeyboardMarkup) or reply_markup is None
        request = {"method": "stopMessageLiveLocation", 'chat_id': chat_id, 'message_id': message_id}
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def send_venue(self, chat_id, latitude: float, longitude: float, title: str, address: str,
                   foursquare_id: str, foursquare_type: str, disable_notification: bool = False,
                   reply_to_message_id: int = None, reply_markup=None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        assert isinstance(latitude, float)
        assert isinstance(longitude, float)
        assert isinstance(title, str)
        assert isinstance(address, str)
        assert isinstance(foursquare_id, str)
        assert isinstance(foursquare_type, str)
        assert isinstance(disable_notification, bool)
        assert isinstance(reply_to_message_id, int) or reply_to_message_id is None
        assert issubclass(type(reply_markup), ReplyMarkups._ReplyMarkup) or reply_markup is None
        request = {"method": "sendVenue", 'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude,
                   'title': title, 'address': address, 'foursquare_id': foursquare_id,
                   'foursquare_type': foursquare_type}
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def send_contact(self, chat_id, phone_number: str, first_name: str, last_name: str = None, vcard: str = None,
                     disable_notification: bool = False, reply_to_message_id: int = None, reply_markup=None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        if isinstance(phone_number, int):
            phone_number = str(phone_number)
        assert isinstance(phone_number, str)
        assert isinstance(first_name, str)
        assert last_name is None or isinstance(last_name, str)
        assert vcard is None or isinstance(vcard, str)
        assert isinstance(disable_notification, bool)
        assert reply_to_message_id is None or isinstance(reply_to_message_id, int)
        assert reply_markup is None or issubclass(type(reply_markup), ReplyMarkups._ReplyMarkup)
        request = {"method": "sendContact", 'chat_id': chat_id, 'phone_number': phone_number, 'first_name': first_name}
        if last_name:
            request['last_name'] = last_name
        if vcard:
            request['vcard'] = vcard
        if disable_notification:
            request['disable_notification'] = disable_notification
        if reply_to_message_id:
            request['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            request['reply_markup'] = reply_markup
        return self.__send_post_request(request)

    def get_user_profile_photos(self, chat_id: int, offset: int = None, limit: int = None) -> dict:
        assert isinstance(chat_id, int)
        assert offset is None or isinstance(offset, int)
        assert limit is None or isinstance(limit, int)
        request = {"method": "getUserProfilePhotos", 'chat_id': chat_id}
        if offset:
            request['offset'] = offset
        if limit:
            request['limit'] = limit
        return self.__send_post_request(request)

    def get_file(self, file_id: str) -> dict:
        assert isinstance(file_id, str)
        return self.__send_post_request({"method": "getFile", 'file_id': file_id})

    def kick_chat_member(self, chat_id, user_id: int, until_date: int = None) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        assert isinstance(user_id, int)
        assert until_date is None or isinstance(until_date, int)
        request = {"method": "kickChatMember", 'user_id': user_id}
        if until_date:
            request['until_date'] = until_date
        return self.__send_post_request(request)

    def unban_chat_member(self, chat_id, user_id: int) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        assert isinstance(user_id, int)
        return self.__send_post_request({"method": "unbanChatMember", 'user_id': user_id})

    def restrict_chat_member(self, chat_id, user_id: int, until_date: int = None, can_send_messages: bool = True,
                             can_send_media_messages: bool = True, can_send_other_messages: bool = True,
                             can_add_web_page_previews: bool = True) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        assert isinstance(user_id, int)
        assert isinstance(until_date, int)
        assert isinstance(can_send_messages, bool)
        assert isinstance(can_send_media_messages, bool)
        assert isinstance(can_send_other_messages, bool)
        assert isinstance(can_add_web_page_previews, bool)
        request = {"method": "restrictChatMember", 'user_id': user_id, 'can_send_messages': can_send_messages,
                   'can_send_media_messages': can_send_media_messages,
                   'can_send_other_messages': can_send_other_messages,
                   'can_add_web_page_previews': can_add_web_page_previews}
        if until_date:
            request['until_date'] = until_date
        return self.__send_post_request(request)

    def promote_chat_member(self, chat_id, user_id: int, can_change_info: bool = False, can_post_messages: bool = False,
                            can_edit_messages: bool = False, can_delete_messages: bool = False,
                            can_invite_users: bool = False, can_restrict_members: bool = False,
                            can_pin_messages: bool = False, can_promote_members: bool = False) -> dict:
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        assert isinstance(user_id, int)
        assert isinstance(can_change_info, bool)
        assert isinstance(can_post_messages, bool)
        assert isinstance(can_edit_messages, bool)
        assert isinstance(can_delete_messages, bool)
        assert isinstance(can_invite_users, bool)
        assert isinstance(can_restrict_members, bool)
        assert isinstance(can_pin_messages, bool)
        assert isinstance(can_promote_members, bool)
        return self.__send_post_request({"method": "promoteChatMember", 'user_id': user_id,
                                         'can_change_info': can_change_info, 'can_post_messages': can_post_messages,
                                         'can_edit_messages': can_edit_messages,
                                         'can_delete_messages': can_delete_messages,
                                         'can_invite_users': can_invite_users,
                                         'can_restrict_members': can_restrict_members,
                                         'can_pin_messages': can_pin_messages,
                                         'can_promote_members': can_promote_members})

    def export_chat_invite_link(self, chat_id):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "exportChatInviteLink", 'chat_id': chat_id})

    # TODO handle input file - photo
    def set_chat_photo(self, chat_id, photo):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
                          'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "setChatPhoto", 'chat_id': chat_id, 'photo': photo})

    def set_chat_title(self, chat_id, title: str):
        assert isinstance(title, str) and 0 < len(title) <= 255, \
            'Chat title must be a string, between 1 and 255 chars length.'
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "setChatTitle", 'chat_id': chat_id, 'title': title})

    def set_chat_description(self, chat_id, description: str):
        assert isinstance(description, str) and 0 < len(description) <= 255, \
            'Chat description must be a string between 1 and 255 chars length.'
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
            'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "setChatDescription", 'chat_id': chat_id,
                                         'description': description})

    def pin_chat_message(self, chat_id, message_id: int, disable_notification: bool = False):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
               'Chat_id must be chat_id or username starting with @'
        assert isinstance(message_id, int)
        assert isinstance(disable_notification, bool)
        request = {"method": "pinChatMessage", 'chat_id': chat_id, 'message_id': message_id}
        if disable_notification:
            request['disable_notification'] = True
        return self.__send_post_request(request)

    def unpin_chat_message(self, chat_id):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
               'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "unpinChatMessage", 'chat_id': chat_id})

    def leave_chat(self, chat_id):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
               'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "leaveChat", 'chat_id': chat_id})

    def get_chat_administrators(self, chat_id):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
               'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "getChatAdministrators", 'chat_id': chat_id})

    def get_chat_member_count(self, chat_id):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
               'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "getChatMembersCount", 'chat_id': chat_id})

    def get_chat_member(self, chat_id, user_id: int):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
               'Chat_id must be chat_id or username starting with @'
        assert isinstance(user_id, int)
        return self.__send_post_request({"method": "getChatMember", 'chat_id': chat_id, 'user_id': user_id})

    def set_chat_sticker_set(self, chat_id, sticker_set_name: str):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
               'Chat_id must be chat_id or username starting with @'
        assert isinstance(sticker_set_name, str)
        return self.__send_post_request({"method": "setChatStickerSet", 'chat_id': chat_id})

    def delete_chat_sticker_set(self, chat_id):
        assert isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id[0] == '@'), \
               'Chat_id must be chat_id or username starting with @'
        return self.__send_post_request({"method": "deleteChatStickerSet", 'chat_id': chat_id})

    def answer_callback_query(self, callback_query_id: str, text: str = None, show_alert: bool = False, url: str = None,
                              cache_time: int = None):
        assert isinstance(callback_query_id, str)
        assert text is None or (isinstance(text, str) and len(text) <= 200)
        assert isinstance(show_alert, bool)
        assert url is None or isinstance(url, str)
        assert cache_time is None or isinstance(cache_time, int)
        request = {"method": "answerCallbackQuery", 'callback_query_id': callback_query_id}
        if text:
            request['text'] = text
        if show_alert:
            request['show_alert'] = True
        if url:
            request['url'] = url
        if cache_time:
            request['cache_time'] = cache_time
        return self.__send_post_request(request)
