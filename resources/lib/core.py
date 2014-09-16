import json
import urllib
import urllib2
import cookielib
from sys import modules
from os.path import join


class Core(object):
    '''
    This class handles loading the cookies and making post and get requests.
    '''

    def __init__(self):
        self.xbmc = modules['__main__'].xbmc
        self.settings = modules['__main__'].settings
        self.cache = modules['__main__'].cache
        self.common = modules['__main__'].common
        self.log = self.common.log

        self.enable_cache = self.settings.getSetting('enable_cache') == 'true'

        self.base_url = 'https://www.funimation.com/{0}'
        self.cookiejar = self._load_cookiejar()
        self.cookie_expired = self._check_cookie()

        cookie_handler = urllib2.HTTPCookieProcessor(self.cookiejar)
        self.open = urllib2.build_opener(cookie_handler).open

    def get(self, endpoint):
        if self.enable_cache:
            return self.cache.cacheFunction(self._request, endpoint)
        else:
            return self._request(endpoint)

    def post(self, endpoint, params):
        if self.enable_cache:
            return self.cache.cacheFunction(self._request, endpoint, params)
        else:
            return self._request(endpoint, params)

    def _request(self, endpoint, params=None):
        if endpoint.startswith('http'):
            url = endpoint
        else:
            url = self.base_url.format(endpoint)

        self.log(url, 4)
        if params is None:
            content = self.open(url).read()
        else:
            content = self.open(url, urllib.urlencode(params)).read()

        self.cookiejar.save()
        return json.loads(content)

    def _load_cookiejar(self):
        cookie_path = self.xbmc.translatePath(
            self.settings.getAddonInfo('profile'))
        cookie_path = join(cookie_path, 'fun-cookiejar.txt')
        cookiejar = cookielib.LWPCookieJar(cookie_path, delayload=True)
        self.log('Loading cookies from :' + repr(cookie_path), 4)
        try:
            cookiejar.load()
        except IOError:
            self.log('Cookie does not exist', 4)
        except cookielib.LoadError:
            self.log('The cookie file is unreadable', 4)

        return cookiejar

    def _check_cookie(self):
        # make sure there are actually cookies
        if self.cookiejar._cookies:
            # get cookie that holds login session. if it has expired cookielib
            # won't load it.
            cookie = self.cookiejar._cookies.get(
                'www.funimation.com').get('/').get('expand')
            if cookie is None:
                return True
            else:
                return False
        else:
            return True
