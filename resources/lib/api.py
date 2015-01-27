from sys import modules, argv
from .core import Core


urls = {
    'shows': 'feeds/ps/shows?ut={ut}&limit={limit}&offset={offset}',
    'episodes': 'feeds/ps/videos?ut={ut}&show_id={show_id}&limit={limit}&offset={offset}',
    'latest': 'feeds/ps/shows?ut={ut}&limit={limit}&offset={offset}&sort={sort}',
    'simulcast': 'feeds/ps/shows?ut={ut}&limit={limit}&offset={offset}&sort={sort}&filter=FilterOptionSimulcast',
    'featured': 'feeds/ps/featured?ut={ut}&limit={limit}&offset={offset}',
    'login': 'feeds/ps/login.json',
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
            sort = 'SortOptionLatestSubscription'
        else:
            ut = 'FunimationUser'
            sort = 'SortOptionLatestFree'
        return locals()
