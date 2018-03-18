class Source(object):

    def __init__(self, notification_queue):
        self.notification_queue = notification_queue

    def get_routers(self):
        return []

    def loop(self):
        pass


class Manager(object):

    def __init__(self, subscribers):
        self.subscribers = subscribers

    def get_routers(self):
        return []

    def loop(self):
        pass


class Pin(object):

    def notify(self, notification):
        pass
