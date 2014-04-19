import sys


class BaseModel(object):
    def __init__(self, json):
        self.plugin = sys.modules['__main__'].plugin
        self.common = sys.modules['__main__'].common
        self.utils = sys.modules['__main__'].utils

        self.json = json

        get = self.json.get
        self.title = get('title')
        self.nid = get('nid')
        self.show_thumbnail = get('show thumbnail')