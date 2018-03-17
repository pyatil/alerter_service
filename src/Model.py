from collections import namedtuple


class DataTypes(object):
    TXT = "text"
    IMG = "image"
    AUDIO = "audio"


Notification = namedtuple("Notification", ["source", "source_type", "type_data", "data", "level_info"])
