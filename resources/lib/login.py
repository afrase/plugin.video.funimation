import sys
import json


class Login(object):

    urls = {'session_url': 'http://www.funimation.com/phunware/system/connect.json'}
    url['login_url'] = 'http://www.funimation.com/phunware/user/login.json'

    def __init__(self):
        self.xbmc = sys.modules['__main__'].xbmc

        self.core = sys.modules['__main__'].core
        self.settings = sys.modules['__main__'].settings
        self.common = sys.modules['__main__'].common

        self.utils = sys.modules['__main__'].utils

    def login(self, params=None):
        if not params: params = {}
        self.common.log('', self.dbg_level)

        user_name = self.settings.user_name()
        user_pass = self.settings.user_password()

        result = ''
        status = 500

        payload = {
            'username': user_name,
            'password': user_pass,
            'sessionid': self._get_session_id(),
        }

        ret = self.core._fetch_page({'url': self.urls['login_url']}, payload)

        if ret['status'] == 200:
            ret = json.loads(ret['content'])
            user = User(ret['user'])

            if user.logged_in:
                sys.modules['__main__'].cookiejar.save()
                self.xbmc.executebuiltin('Container.Refresh')
                return user, 200

        self.xbmc.executebuiltin('Container.Refresh')
        return result, status

    def authorize(self):
        self.settings.set_setting('session_id', '')
        self.settings.set_setting('session_id_refresh', '')
        result, status = self._http_login({'new': 'true'})
        if status == 200:
            result, status = self._api_login()

        return result, status

    def _get_session_id(self):
        ret = self.core._fetch_page({'url': self.urls['session_url']})
        return json.loads(ret['content'])['sessid']