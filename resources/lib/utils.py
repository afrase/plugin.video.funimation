import sys
import os

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
        self.plugin = sys.modules['__main__'].plugin
        self.language = sys.modules['__main__'].language
        self.common = sys.modules['__main__'].common

    def get_thumbnail(self, title):
        if not title:
            title = 'DefaultFolder'
        thumbnail_path = os.path.join(self.plugin.getAddonInfo('path'), 'thumbnails')
        thumbnail = os.path.join(thumbnail_path, title + '.png')
        if not os.path.isfile(thumbnail):
            thumbnail = 'DefaultFolder.png'

        return thumbnail

    def show_message(self, message, title=None, icon=None):
        self.common.log(repr(title) + " - " + repr(message), 5)
        duration = ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10][int(self.plugin.getSetting('notification_length'))]) * 1000
        if not title:
            title = self.plugin.getAddonInfo('name')
        if not icon:
            icon = self.plugin.getAddonInfo('icon')
        self.xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (title, message, duration, icon))

    def show_error_message(self, result=None, title=None):
        if not title:
            title = self.get_string('error')

        if result:
            self.show_message(result, title)
        else:
            self.show_message(self.get_string('unknown_error'), title)

    def build_item_url(self, item_params=None, url=''):
        self.common.log('url: %s items: %s' % (repr(url), repr(item_params)), 9)
        if not item_params: item_params = {}

        blacklist = ('path', 'thumbnail', 'icon', 'Title', 'Title2')

        for key, value in item_params.items():
            if key not in blacklist:
                url += key + '=' + value + '&'
        return url

    def add_next_folder(self, items=None, params=None):
        if not params: params = {}
        if not items: items = []

        get = params.get
        item = {"Title": self.get_string('more_results'), "thumbnail": "next", "next": "true", "page": str(int(get("page", "0")) + 1)}
        for k, v in params.items():
            if k != "thumbnail" and k != "Title" and k != "page" and k != "new_results_function":
                item[k] = v
        items.append(item)

    def get_string(self, string_id):
        if string_id in STRINGS:
            string = self.language(STRINGS[string_id]).encode('utf-8')
            self.common.log('%s translates to %s' % (STRINGS[string_id], string), 5)
            return string
        else:
            self.common.log('String is missing: %s' % string_id, 5)
            return string_id

    def stream_url(self, video_id, hd=False):
        # TODO: figure out the max quality
        if hd:
            quality = '3500'
        else:
            quality = '2000'

        base_url = 'http://wpc.8c48.edgecastcdn.net'
        uid = '9b303b6c62204a9dcb5ce5f5c607'
        url = '%s/038C48/SV/480/%s/%s-480-%sK.mp4.m3u8?%s' % (
            base_url, video_id, video_id, quality, uid)
        self.common.log(url, 9)
        return url

    @staticmethod
    def to_minutes(t):
        if len(t.split(':')) == 2:
            m, s = [int(i) for i in t.split(':')]
            return (60 * m + s) / 60
        elif len(t.split(':')) == 3:
            h, m, s = [int(i) for i in t.split(':')]
            return (3600 * h + 60 * m + s) / 60