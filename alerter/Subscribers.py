import os
import json
import aiofiles
from collections import namedtuple
from alerter.config import DATA_PATH

SUBSCRIBER_FILE = os.path.join(DATA_PATH, "subscribers.json")


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


Subscriber = namedtuple("Subscriber", ["user_id", "pin_type", "source_intresting", "level_info", "regex"])


class FileSubscribers(object):
    def __init__(self):
        subscribers = get_persistent_data(SUBSCRIBER_FILE, {})
        self.subscribers = {k: [Subscriber(*s) for s in v] for k, v in subscribers.items()}

    async def add(self, subscriber):
        if subscriber.user_id not in self.subscribers:
            self.subscribers[subscriber.user_id] = [subscriber]
        else:
            self.subscribers[subscriber.user_id].append(subscriber)
        await persist_data(SUBSCRIBER_FILE, self.subscribers)

    def __iter__(self):
        return iter(self.subscribers.items())


subscribers = FileSubscribers()
