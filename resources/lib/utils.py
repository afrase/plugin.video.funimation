import sys

STRINGS = {
    'tv_shows': 30001,
    'episodes': 30002,
    'movies': 30003,
    'trailers': 30004,
    'clips': 30005,
    'search': 30006,
    'clear_cache': 30007,
    'addon_settings': 30100,
    'show_list_error': 30200,
    'episode_list_error': 30201,
    'login_failed': 30202,
    'clear_cache_msg': 30300,
}


class Utils(object):
    __plugin__ = None

    DEBUG = 0
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

    def __init__(self):
        try:
            self.__plugin__ = sys.modules['__main__'].plugin
        except:
            # we are running from the command line
            self.__plugin__ = sys.modules['addon'].plugin

    def get_plugin(self):
        return self.__plugin__

    def get_string(self, string_id):
        if string_id in STRINGS:
            return self.__plugin__.get_string(STRINGS[string_id]).encode('utf-8')
        else:
            self.__plugin__.log.info('String is missing: %s' % string_id)
            return string_id

    def get_log(self, log_type=INFO):
        if log_type == self.INFO:
            return self.__plugin__.log.info
        elif log_type == self.DEBUG:
            return self.__plugin__.log.debug
        elif log_type == self.WARNING:
            return self.__plugin__.log.warning
        elif log_type == self.ERROR:
            return self.__plugin__.log.error
        elif log_type == self.CRITICAL:
            return self.__plugin__.critical
        else:
            return None

    def get_show_cache(self):
        return self.__plugin__.get_storage('shows')

    def get_episode_cache(self, e_id):
        cache_name = 'episodes_%s' % e_id
        self.add_to_cache_list(cache_name)
        return self.__plugin__.get_storage(cache_name)

    def get_user_cache(self):
        return self.__plugin__.get_storage('user')

    def get_sessionid_cache(self):
        return self.__plugin__.get_storage('sessionid', TTL=60)

    def get_cookie_cache(self):
        return self.__plugin__.get_storage('cookies')

    def get_cache_list(self):
        return self.__plugin__.get_storage('cache_list')

    def add_to_cache_list(self, name):
        if name not in self.get_cache_list():
            self.get_cache_list().items().append(name)

    # clear functions

    def clear_cache(self):
        self.__plugin__.log.info('Clearing all cache')
        self.clear_show_cache()
        self.clear_episode_cache()
        self.clear_user_cache()
        self.clear_sessionid_cache()
        self.clear_cookie_cache()
        self.__plugin__.clear_function_cache()

    def clear_show_cache(self):
        self.__clear__(self.get_show_cache())

    def clear_episode_cache(self):
        for i in self.get_cache_list():
            self.__clear__(self.get_episode_cache(i))

    def clear_user_cache(self):
        self.__clear__(self.get_user_cache())

    def clear_sessionid_cache(self):
        self.__clear__(self.get_sessionid_cache())

    def clear_cookie_cache(self):
        self.__clear__(self.get_cookie_cache())

    def __clear__(self, cache):
        cache.clear()
        self.__sync__(cache)

    def __sync__(self, cache):
        cache.sync()

