import json
from django.utils import timezone
import redis


def get_redis_client():
    return redis.StrictRedis()


def get_public_chat_channel():
    return 'public_chat'


class RedisChatPublisherSubscriber(object):
    def __init__(self):
        self._client = get_redis_client()
        self.subscription = None

    def _subscribe_to_channel(self, channel):
        if self.subscription is None:
            self.subscription = self._client.pubsub()
        self.subscription.subscribe(channel)

    def listen(self):
        return self.subscription.listen()

    # Public chat channel
    def subscribe_to_public_chat_channel(self):
        self._subscribe_to_channel(get_public_chat_channel())

    def publish_to_public_chat_channel(self, nickname, message):
        chat = json.dumps({'message': message, 'nickname': nickname})
        self._client.publish(get_public_chat_channel(), chat)

    def close(self):
        if self.subscription:
            self.subscription.close()
