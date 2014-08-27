from sys import modules


class BaseModel(object):

    def __init__(self, json):
        self.utils = modules['__main__'].utils

        self.json = json

        get = self.json.get
        self.title = get('title')
        self.nid = get('nid')
        self.show_thumbnail = get('show thumbnail')
