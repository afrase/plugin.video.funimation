import sys


class BaseController(object):
    def __init__(self):
        self._plugin = sys.modules['__main__'].plugin
        self._common = sys.modules['__main__'].common
        self._utils = sys.modules['__main__'].utils

        self._items = []

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def has_more(self):
        # seems the api only returns 50 episodes at a time
        return len(self._items) >= 50