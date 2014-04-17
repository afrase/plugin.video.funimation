import sys


class BaseController(object):
    def __init__(self):
        self.plugin = sys.modules['__main__'].plugin
        self.common = sys.modules['__main__'].common
        self.utils = sys.modules['__main__'].utils