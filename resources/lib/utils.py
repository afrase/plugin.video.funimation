import sys
import os
import time
from functools import wraps

STRINGS = {
    'shows': 30010,
    'search': 30011,
    'episodes': 30012,
    'movies': 30013,
    'trailers': 30014,
    'clips': 30015,
    'more_results': 30016,

    # messages
    'error': 30600,
    'unknown_error': 30601,
    'no_episodes': 30603,
    'no_movies': 30604,
    'no_trailers': 30605,
    'no_clips': 30606,

    # genres
    'action': 30700,
    'adventure': 30701,
    'bishonen': 30702,
    'bishoujo': 30703,
    'comedy': 30704,
    'cyberpunk': 30705,
    'drama': 30706,
    'fan_service': 30707,
    'fantasy': 30708,
    'harem': 30709,
    'historical': 30710,
    'horror': 30711,
    'live_action': 30712,
    'magical_girl': 30713,
    'martial_arts': 30714,
    'mecha': 30715,
    'moe': 30716,
    'mystery': 30717,
    'reverse_harem': 30718,
    'romance': 30719,
    'school': 30720,
    'scifi': 30721,
    'shonen': 30722,
    'slice_of_life': 30723,
    'space': 30724,
    'sports': 30725,
    'super_power': 30726,
    'supernatural': 30727,
    'yuri': 30728,
}


class Utils(object):
    def __init__(self):
        self.xbmc = sys.modules['__main__'].xbmc
        self.settings = sys.modules['__main__'].settings
        self.language = sys.modules['__main__'].language
        self.log = sys.modules['__main__'].common.log

    def get_thumbnail(self, title=None):
        if title is None:
            title = 'DefaultFolder'
        thumbnail_path = os.path.join(self.settings.getAddonInfo('path'), 'thumbnails')
        thumbnail = os.path.join(thumbnail_path, title + '.png')
        if not os.path.isfile(thumbnail):
            thumbnail = 'DefaultFolder.png'
        self.log('Thumbnail: ' + thumbnail, 5)
        return thumbnail

    def show_message(self, msg, title=None, icon=None):
        dur = int(self.settings.getSetting('notification_length'))
        if title is None:
            title = self.settings.getAddonInfo('name')
        if icon is None:
            icon = self.settings.getAddonInfo('icon')

        self.xbmc.executebuiltin(
            'Notification({title}, {msg}, {dur}, {icon})'.format(**locals()))

    def show_error_message(self, result=None, title=None):
        if title is None:
            title = self.get_string('error')
        if result is None:
            result = self.get_string('unknown_error')
        self.show_message(result, title)

    def build_item_url(self, item_params=None, url=''):
        self.log('url: %s items: %s' % (repr(url), repr(item_params)), 5)
        blacklist = ('path', 'thumbnail', 'icon', 'Title', 'Title2')
        if item_params is None:
            item_params = {}

        for key, value in item_params.items():
            if key not in blacklist:
                url += key + '=' + value + '&'

        return url

    def add_next_folder(self, items=None, params=None):
        if params is None:
            params = {}
        if items is None:
            items = []

        get = params.get
        item = {"Title": self.get_string('more_results'), "thumbnail": "next", "next": "true", "page": str(int(get("page", "0")) + 1)}
        for k, v in params.items():
            if k != "thumbnail" and k != "Title" and k != "page" and k != "new_results_function":
                item[k] = v
        items.append(item)

    def get_string(self, string_id):
        if string_id in STRINGS:
            string = self.language(STRINGS[string_id]).encode('utf-8')
            self.log('%s translates to %s' % (STRINGS[string_id], string), 5)
            return string
        else:
            self.log('String is missing: ' + string_id, 5)
            return string_id

    def stream_url(self, video_id, hd=False):
        # TODO: figure out the max quality
        if hd:
            quality = '3500'
        else:
            quality = '2000'

        base_url = 'http://wpc.8c48.edgecastcdn.net'
        # this value doesn't seem to change
        uid = '9b303b6c62204a9dcb5ce5f5c607'
        url = '{base_url}/038C48/SV/480/{video_id}/{video_id}-480-{quality}K.mp4.m3u8?{uid}'.format(**locals())
        self.log(url, 5)
        return url

    @staticmethod
    def to_minutes(t):
        if len(t.split(':')) == 2:
            m, s = [int(i) for i in t.split(':')]
            return (60 * m + s) / 60
        elif len(t.split(':')) == 3:
            h, m, s = [int(i) for i in t.split(':')]
            return (3600 * h + 60 * m + s) / 60

    @staticmethod
    def timethis(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            f = func(*args, **kwargs)
            end = time.time()
            sys.modules['__main__'].common.log('{0}.{1} : {2} sec'.format(
                func.__module__, func.__name__, end - start))
            return f
        return wrapper


class Timer:

    def __init__(self, func=time.time):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    @property
    def running(self):
        return self._start is not None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
