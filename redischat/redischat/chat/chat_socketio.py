import json
from redis import ConnectionError
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from .redis_chat_pubsub import RedisChatPublisherSubscriber


class ChatNamespace(BaseNamespace, BroadcastMixin):
    def __init__(self, environ, ns_name, request=None):
        self._pub_sub_client = RedisChatPublisherSubscriber()
        super(ChatNamespace, self).__init__(environ, ns_name, request)

    def recv_connect(self):
        self._pub_sub_client.subscribe_to_public_chat_channel()
        self.spawn(self.listen)

    def handle_chat(self, data):
        self.emit('on_chat_message', data)

    def on_chat(self, nickname, message):
        self._pub_sub_client.publish_to_public_chat_channel(nickname, message)

    def listen(self):
        if self._pub_sub_client.subscription is None:
            return
        try:
            for notification in self._pub_sub_client.listen():
                if notification['type'] == 'message':
                    data = json.loads(notification['data'])
                    self.handle_chat(data)
        except ConnectionError:
            try:
                self._pub_sub_client.close()
            except:
                pass

    def recv_disconnect(self):
        super(ChatNamespace, self).recv_disconnect()
        self._pub_sub_client.close()
