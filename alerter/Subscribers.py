import os
import json
import aiofiles
from contextlib import suppress
from alerter.config import DATA_PATH

SUBSCRIBER_FILE = os.path.join(DATA_PATH, "subscribers.json")


def to_json(obj):
    if hasattr(obj, "to_json"):
        return obj.to_json()
    else:
        return json.dumps(obj)


def get_persistent_data(path_data, default=None):
    with suppress(FileExistsError):
        os.mkdir(os.path.dirname(SUBSCRIBER_FILE))
    try:
        with open(path_data) as fp:
            return json.load(fp)
    except:
        return default


async def persist_data(path_data, data):
    async with aiofiles.open(path_data, 'w') as fp:
        data = json.dumps(data, default=to_json)
        await fp.write(data)


class Subscriber(object):

    def __init__(self, user_id, pin_type, source_intresting, level_info, regex):
        self.user_id = str(user_id)
        self.pin_type = pin_type
        self.source_intresting = source_intresting
        self.level_info = level_info
        self.regex = regex
        self._tuple = (self.user_id, self.pin_type, self.source_intresting, self.level_info, self.regex)

    def to_json(self):
        return json.dumps(self._tuple)

    def __iter__(self):
        return iter(self._tuple)


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

    async def remove(self, user_id, sub_idx):
        subs = self.subscribers.get(str(user_id), [])
        sub = subs.pop(sub_idx)
        await persist_data(SUBSCRIBER_FILE, self.subscribers)
        return sub.regex

    async def get_subscriptions(self, user_id):
        subs = self.subscribers.get(str(user_id), [])
        return subs

    def __iter__(self):
        return iter(self.subscribers.items())


subscribers = FileSubscribers()
