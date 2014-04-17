import sys


class Settings(object):
    def __init__(self):
        self.plugin = sys.modules['__main__'].plugin
        self.dbg = sys.modules['__main__'].dbg

    def user_name(self):
        return self.plugin.getSetting('username')

    def user_password(self):
        return self.plugin.getSetting('password')

    def debug_is_enabled(self):
        return self.plugin.getSetting('debug') == 'true'

    def refresh_session(self):
        return self.plugin.getSetting('session_id_refresh')

    def set_setting(self, setting, value):
        self.plugin.setSetting(setting, value)