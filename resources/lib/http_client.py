import cookielib
import json
import os
import sys
import urllib
import urllib2
import xbmcvfs


class HTTPClient(object):
    def __init__(self):
        self.__xbmc__ = sys.modules['__main__'].xbmc
        self.__plugin__ = sys.modules['__main__'].plugin
        self.__settings__ = sys.modules['__main__'].settings
        self.__common__ = sys.modules['__main__'].common
        self.__log__ = self.__common__.log

        cookie_path = self.__xbmc__.translatePath(self.__plugin__.getAddonInfo('profile'))
        cookie_path = os.path.join(cookie_path, 'fun-cookiejar.txt')
        self.__log__('Loading cookies from :' + repr(cookie_path), 5)
        self.__cookiejar__ = cookielib.LWPCookieJar(cookie_path)

        self.user = None

        if xbmcvfs.exists(cookie_path):
            try:
                self.__cookiejar__.load()
            except cookielib.LoadError:
                pass
        else:
            self.__cookiejar__.save()

        cookie_handler = urllib2.HTTPCookieProcessor(self.__cookiejar__)
        self.__opener__ = urllib2.build_opener(cookie_handler)

        self.urls = {
            'connect': 'http://www.funimation.com/phunware/system/connect.json',
            'login': 'http://www.funimation.com/phunware/user/login.json',
        }

    def get(self, url):
        url = self.__url__(url)
        resp = self.__opener__.open(url)
        return json.loads(''.join(resp.readlines())), resp.code

    def post(self, url, data=None):
        data = [] if data is None else urllib.urlencode(data)
        resp = self.__opener__.open(self.__url__(url), data)
        return json.loads(''.join(resp.readlines())), resp.code

    def get_cookies_str(self):
        return self.__cookiejar__.as_lwp_str()

    def save(self):
        self.__cookiejar__.save()

    def __url__(self, url):
        if url.startswith('/'):
            url = 'http://www.funimation.com' + url
        self.__log__(url, 5)
        return url