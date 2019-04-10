

class Entity:

    __slots__ = 'offset', 'length', 'type'

    def __init__(self, entity: dict):
        self.offset = entity.get('offset', None)
        self.length = entity.get('length', None)
        self.type = entity.get('type', None)


class Chat:

    __slots__ = 'id', 'first_name', 'last_name', 'username', 'type', 'title'

    def __init__(self, chat: dict):
        self.id = chat.get('id', None)
        self.first_name = chat.get('first_name', None)
        self.last_name = chat.get('last_name', None)
        self.username = chat.get('username', None)
        self.type = chat.get('type', None)
        self.title = chat.get('title', None)


class FromUser:

    __slots__ = 'id', 'is_bot', 'first_name', 'last_name', 'username', 'language_code'

    def __init__(self, from_user: dict):
        self.id = from_user.get('id', None)
        self.is_bot = from_user.get('is_bot', None)
        self.first_name = from_user.get('first_name', None)
        self.last_name = from_user.get('last_name', None)
        self.username = from_user.get('username', None)
        self.language_code = from_user.get('language_code', None)


class Message:

    __slots__ = 'message_id', 'from_user', 'chat', 'date', 'text', 'entities', 'forward_from_message_id', \
                'forward_date', 'media_group_id'

    def __init__(self, message: dict):
        self.message_id = message.get('message_id', None)
        self.from_user = FromUser(message.get('from', None))
        self.chat = Chat(message.get('chat', None))
        self.date = message.get('date', None)
        self.text = message.get('text', None)
        self.entities = [message.get('entities', None)]
        self.forward_from_message_id = message.get('forward_from_message_id', None)
        self.forward_date = message.get('forward_date', None)
        self.media_group_id = message.get('media_group_id', None)


class Update:

    __slots__ = 'update'

    def __init__(self, update: dict):
        self.update = update

    def update_id(self) -> int:
        return self.update['id']

    def message(self) -> Message:
        return Message(self.update['message'])




