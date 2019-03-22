import json
import requests
import urllib


class BotAPI:

    def __init__(self, token, last_update_id=-1):
        self.url = 'https://api.telegram.org/bot' + token + '/'
        self.last_update_id = last_update_id

    def send_post_request(self, parameters_dict):
        """Sends request to bot and returns json file with response
        Args: parameters_dict is a dictionary with parameters"""
        return json.loads(requests.post(self.url, json=parameters_dict).content.decode("utf8"))

    def get_bot_details(self):
        return self.send_post_request({"method": "getme"})

    def get_updates(self, offset=True, timeout=100):
        d = {"timeout": timeout, "method": "getUpdates"}
        if offset is True:
            if self.last_update_id > -1:
                d["offset"] = self.last_update_id
        elif type(offset) == 'int':
            d["offset"] = offset
        result = self.send_post_request(d)
        for update_id in result["result"]:
            if int(update_id) > self.last_update_id:
                self.last_update_id = int(update_id)
        return result

    def send_message(self, text, chat_id):
        text = urllib.parse.quote_plus(text)
        self.send_post_request({"method": "sendMessage", "text": text, "chat_id": chat_id})




