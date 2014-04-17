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
    'error': 30600,
    'unknown_error': 30601,

}


class Utils(object):
    def __init__(self):
        self.xbmc = sys.modules['__main__'].xbmc
        self.plugin = sys.modules['__main__'].plugin
        self.language = sys.modules['__main__'].language
        self.common = sys.modules['__main__'].common
        self.dbg = sys.modules['__main__'].dbg

        self.thumbnail_path = os.path.join(self.plugin.getAddonInfo('path'), 'thumbnails')

    def get_thumbnail(self, title):
        if not title:
            title = 'DefaultFolder'

        thumbnail = os.path.join(self.thumbnail_path, title + '.png')
        if not os.path.isfile(thumbnail):
            thumbnail = 'DefaultFolder.png'

        return thumbnail

    def show_message(self, heading, message):
        self.common.log(repr(type(heading)) + " - " + repr(type(message)), 5)
        duration = ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10][int(self.plugin.getSetting('notification_length'))]) * 1000
        self.xbmc.executebuiltin((u'XBMC.Notification("%s", "%s", %s)' % (heading, message, duration)).encode())

    def show_error_message(self, result=None, title=None):
        """
        Shows an error message.

        :param result: the content of the message. If none then and unknown_error message is displayed
        :param title: the title of the message
        :type result: str
        :type title: str
        """
        if not title:
            title = self.get_string('error')

        if result:
            self.show_message(title, result)
        else:
            self.show_message(title, self.get_string('unknown_error'))

    def build_item_url(self, item_params=None, url=''):
        self.common.log('url: %s items: %s' % (repr(url), repr(item_params)), 9)
        if not item_params: item_params = {}

        blacklist = ('path', 'thumbnail', 'icon', 'Title')

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
            self.common.log('%s translates to %s' % (STRINGS[string_id], string))
            return string
        else:
            self.common.log('String is missing: %s' % string_id)
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