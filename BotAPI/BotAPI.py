import json
import requests
import urllib


def send_get_request(url):
    """url is request, returns json file with response"""
    return json.loads(requests.get(url).content.decode("utf8"))


class BotAPI:

    def __init__(self, token, last_update_id=-1):
        self.token = token
        self.last_update_id = last_update_id

    def get_bot_details(self):
        return send_get_request('https://api.telegram.org/bot'+self.token+'/getme')

    def get_updates(self, offset=True, timeout=100):
        if offset is True:
            if self.last_update_id > -1:
                offset = '?offset=' + self.last_update_id
            else:
                offset = ''
        elif offset is False:
            offset = ''
        else:
            offset = '?offset=' + offset

        result = send_get_request('https://api.telegram.org/bot' + self.token + '/getUpdates?timeout=' + timeout +
                                  offset)

        for update_id in result["result"]:
            if int(update_id) > self.last_update_id:
                self.last_update_id = int(update_id)
        return result

    def send_message(self, text, chat_id):
        text = urllib.parse.quote_plus(text)
        send_get_request('https://api.telegram.org/bot' + self.token + '/sendMessage?text='+text+'&chat_id='+chat_id)


