from sys import modules


class BaseController(object):

    def __init__(self):
        self.settings = modules['__main__'].settings
        self.utils = modules['__main__'].utils
        self.log = modules['__main__'].common.log

        self._items = []

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def has_more(self):
        # seems the api only returns 50 episodes at a time
        return len(self._items) >= 50
