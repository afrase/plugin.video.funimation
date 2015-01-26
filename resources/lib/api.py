from sys import modules, argv
from .core import Core


rating_type = ['tvpg', 'tv14', 'tvma', 'nr', 'pg', 'pg13', 'r', 'all']
sort_types = ['alpha', 'date', 'dvd', 'now', 'soon', 'votes', 'episode',
              'title', 'sequence']
genre_types = ['all', 'action', 'adventure', 'bishonen', 'bishoujo', 'comedy',
               'cyberpunk', 'drama', 'fan service', 'fantasy', 'harem',
               'historical', 'horror', 'live action', 'magical girl',
               'martial arts', 'mecha', 'moe', 'mystery', 'reverse harem',
               'romance', 'school', 'sci fi', 'shonen', 'slice of life',
               'space', 'sports', 'super power', 'supernatural', 'yuri']

urls = {
    'shows': 'feeds/ps/shows?ut={ut}&limit={limit}&offset={offset}',
    'episodes': 'feeds/ps/videos?ut={ut}&show_id={show_id}&limit={limit}&offset={offset}',
    'featured': 'feeds/ps/featured?{0}',
    'login': 'feeds/ps/login.json',
    'latest': 'feeds/ps/shows?ut={ut}&limit={limit}&offset={offset}&sort=SortOptionLatestSubscription',
}


class Api(Core):

    def __init__(self):
        super(Api, self).__init__()
        self.logged_in = False
        self.subscribed = self.settings.getSetting('subsciber') == 'true'
        self.login()

    def get_data(self, endpoint, params):
        params = self._check_params(**params)
        url = urls[endpoint].format(**params)
        self.log('ENDPOINT: %s PARAMS: %s URL: %s' % (repr(endpoint), repr(params), url))
        return self._get_data(url)

    def login(self):
        if self.cookie_expired:
            self._login()
        else:
            self.logged_in = True

    def _login(self):
        user = self.settings.getSetting('username')
        passwd = self.settings.getSetting('password')
        if user and passwd:
            payload = {'username': user, 'password': passwd, 'playstation_id': '',}
            resp = self.post(urls['login'], payload, False)
            if resp.get('user_type') == 'FUNIMATION_SUBSCRIPTION_USER':
                self.logged_in = True
                self.common.show_message('Successfully logged in as %s' % user, 'Login Successful')
            else:
                self.logged_in = False
                self.common.show_error_message('Unknown login error')

    def _check_subscriber(self, resp=None):
        if resp is None:
            self.settings.setSetting('subsciber', 'false')
            self.subscribed = False
        else:
            try:
                if resp['roles'].values()[0] == u'Subscriber':
                    self.settings.setSetting('subsciber', 'true')
                    self.subscribed = True
                else:
                    self.settings.setSetting('subsciber', 'false')
                    self.subscribed = False
            except:
                self.settings.setSetting('subsciber', 'false')
                self.subscribed = False

    def _get_data(self, url):
        try:
            resp = self.get(url)
            data = self.common.process_response(resp)
            return self.common.filter_response(data)
        except Exception, e:
            self.log('ERROR: %s URL: %s ' % (e, self.base_url.format(url)))
            return []

    def _check_params(self, limit=1000, offset=0, show_id=None, **kwargs):
        if self.logged_in:
            ut = 'FunimationSubscriptionUser'
        else:
            ut = 'SomethingElse'
        return locals()



class PS3API(object):
    base_url = 'https://www.funimation.com/{0}'

    urls = {
        'shows': 'feeds/ps/shows?{0}',
        'episodes': 'feeds/ps/videos?{0}',
        'featured': 'feeds/ps/featured?{0}',
    }

    def __init__(self, limit=1000):
        super(PS3API, self).__init__()
        self.limit = limit
        cookie_handler = urllib2.HTTPCookieProcessor()
        self.opener = urllib2.build_opener(cookie_handler)
        self.open = self.opener.open

    def get_data(self, endpoint, params):
        return self.get_shows()

    def _build_uri(self, endpoint, params=None):
        url_params = {'ut': 'FunimationSubscriptionUser', 'limit': self.limit, 'offset': 0}
        if params is not None:
            url_params.update(params)
        return self.urls[endpoint].format(urllib.urlencode(url_params))

    def _request(self, uri, params=None):
        url = self.base_url.format(uri)
        if params is None:
            content = self.open(url).read()
        else:
            content = self.open(url, json.dumps(params)).read()
        return json.loads(content)

    def login(self):
        payload = {
            'username': 'bitness64',
            'password': 'v876fQCWFSgH4Hpe',
            'playstation_id': '',
        }
        return self._request('/feeds/ps/login.json', payload)

    def get_shows(self):
        return self._request(self._build_uri('shows'))

    def get_episodes(self, eid):
        return self.get_data(self._build_uri('episodes', {'show_id': eid}))['videos']

    def get_featured(self):
        return self.get_data(self._build_uri('featured'))

    def get_latest(self):
        return self.get_data(self._build_uri('shows', {'sort': 'SortOptionLatestSubscription'}))

    def get_simulcast(self):
        return self.get_data(self._build_uri('shows', {'filter': 'FilterOptionSimulcast', 'sort': 'SortOptionLatestSubscription'}))


if __name__ == '__main__':
    api = PS3API()
    print(api.login())
    # show = api.get_shows()[86]
    # print(show)
    # print(api.get_featured()[0])
    # print(api.get_latest()[0])
    # print(api.get_simulcast()[0])
    # print(api.get_episodes(show['asset_id'])[0])
