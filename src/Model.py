import os
import json
import aiofiles
from collections import namedtuple

PERSISTENT_DIR = os.path.dirname(__file__)
SUBSCRIBER_FILE = os.path.join(PERSISTENT_DIR, "subscribers.json")


def get_persistent_data(path_data, default=None):
    try:
        with open(path_data) as fp:
            return json.load(fp)
    except:
        return default


async def persist_data(path_data, data):
    async with aiofiles.open(path_data, 'w') as fp:
        data = json.dumps(data)
        await fp.write(data)


class DataTypes(object):
    TXT = "text"
    IMG = "image"
    AUDIO = "audio"


Notification = namedtuple("Notification", ["source", "source_type", "type_data", "data", "level_info"])


Subscriber = namedtuple("Subscriber", ["pin_id", "pin_type", "source_intresting", "level_info", "regex"])


class Subscribers(object):
    def __init__(self):
        subscribers = get_persistent_data(SUBSCRIBER_FILE, set())
        self.subscribers = set(Subscriber(*elem) for elem in subscribers)

    async def add(self, subscriber):
        self.subscribers.add(subscriber)
        await persist_data(SUBSCRIBER_FILE, list(self.subscribers))

    def __iter__(self):
        return iter(self.subscribers)


subscribers = Subscribers()
print("inited model")
