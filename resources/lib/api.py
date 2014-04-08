import requests
import inspect


class FunimationApi():
    BASE_URL = 'http://www.funimation.com'
    USER_AGENT = 'FUNimation/858 CFNetwork/672.1.13 Darwin/14.0.0'

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.logged_in = False

        self.req = requests.Session()
        self.req.headers = {'User-Agent': self.USER_AGENT}
        self.session_id = None

    def login(self):
        if not self.logged_in:
            payload = {
                'username': self.username,
                'password': self.password,
                'sessionid': self.get_session_id(),
            }
            resp = self.req.post(
                self.BASE_URL + '/phunware/user/login.json', payload).json()
            if 'incorrect' not in resp['user']['session']:
                self.log('Logged in as %s' % self.username)
                self.logged_in = True
                return self
            else:
                self.log('Log in failed for %s \'%s\'' % (
                    self.username, resp['user']['session']))
                self.logged_in = False
                return self
        else:
            return self

    def get_shows(self):
        try:
            return self.req.get(self._url(
                '/mobile/shows.json/alpha/asc/nl/all/all')
            ).json()
        except:
            return None

    def search_shows(self, term):
        try:
            return self.req.get(self._url(
                '/mobile/shows.json/alpha/asc/nl/all/all'
            ), {'keys': term}).json()
        except:
            return None

    def get_episodes(self, eid, page=0, items=None):
        if not items: items = {'nodes': []}
        try:
            results = self.req.get(self._url(
                '/mobile/episodes.json/subscription/sequence/asc/all/%s/all/all' % eid), params={'page': page}
            ).json()
            if len(results) > 0:
                items['nodes'] += results['nodes']
                return self.get_episodes(eid, page + 1, items)
            else:
                return items
        except:
            return None

    def get_trailers(self, tid):
        try:
            return self.req.get(self._url(
                '/mobile/trailers.json/date/desc/%s/all/all' % tid)
            ).json()
        except:
            return None

    def get_clips(self, cid):
        try:
            return self.req.get(self._url(
                '/mobile/clips.json/date/desc/%s/all/all' % cid)
            ).json()
        except:
            return None

    def get_movies(self, mid):
        try:
            return self.req.get(self._url(
                '/mobile/movies.json/date/desc/%s/all/all' % mid)
            ).json()
        except:
            return None

    def get_session_id(self):
        if self.session_id:
            return self.session_id
        else:
            sessid = self.req.post(
                self.BASE_URL + '/phunware/system/connect.json'
            ).json()['sessid']
            self.log('Got session ID: %s' % sessid)
            return sessid

    def log(self, text):
        print u'[%s.%s]: %s' % (
            self.__class__.__name__,
            inspect.currentframe().f_back.f_code.co_name,
            text)

    def _url(self, path):
        self.login()
        self.log('url: %s' % path)
        return self.BASE_URL + path