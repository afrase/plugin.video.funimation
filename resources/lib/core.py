import json
import urllib
import urllib2
import cookielib
from sys import modules
from os.path import join, exists
from os import makedirs
from .common import timethis

class Core(object):

    '''
    This class handles loading the cookies and making post and get requests.
    '''

    def __init__(self):
        super(Core, self).__init__()
        self.xbmc = modules['__main__'].xbmc
        self.settings = modules['__main__'].settings
        self.cache = modules['__main__'].cache
        self.common = modules['__main__'].common
        self.log = self.common.log

        self.enable_cache = self.settings.getSetting('enable_cache') == 'true'

        self.base_url = 'https://www.funimation.com/{0}'
        self.cookiejar = self._load_cookiejar()
        self.cookie_expired = self._is_session_expired()

        cookie_handler = urllib2.HTTPCookieProcessor(self.cookiejar)
        self.opener = urllib2.build_opener(cookie_handler)
        self.opener.addheaders = [('User-Agent', 'Sony-PS3')]
        self.open = self.opener.open

    def get(self, endpoint, cache=True):
        if self.enable_cache and cache:
            return self.cache.cacheFunction(self._request, endpoint)
        else:
            return self._request(endpoint)

    def post(self, endpoint, params, cache=True):
        if self.enable_cache and cache:
            return self.cache.cacheFunction(self._request, endpoint, params)
        else:
            return self._request(endpoint, params)

    @timethis
    def _request(self, endpoint, params=None):
        if endpoint.startswith('http'):
            url = endpoint
        else:
            url = self.base_url.format(endpoint)

        self.log(url, self.common.DEBUG)
        if params is None:
            content = self.open(url).read()
        else:
            content = self.open(url, json.dumps(params)).read()

        self.cookiejar.save()
        return json.loads(content)

    def _load_cookiejar(self):
        cookie_path = self.xbmc.translatePath(
            self.settings.getAddonInfo('profile'))
        if not exists(cookie_path):
            makedirs(cookie_path)
        cookie_path = join(cookie_path, 'fun-cookiejar.txt')
        cookiejar = cookielib.LWPCookieJar(cookie_path, delayload=True)
        self.log('Cookie file :' + repr(cookie_path), self.common.DEBUG)
        try:
            cookiejar.load()
        except IOError:
            self.log('Cookie does not exist', self.common.WARN)
        except cookielib.LoadError:
            self.log('The cookie file is unreadable', self.common.ERROR)

        return cookiejar

    def _is_session_expired(self):
        # cookielib wont load expired cookies
        try:
            self.cookiejar._cookies['www.funimation.com']['/']['ci_session']
            return False
        except:
            return True
