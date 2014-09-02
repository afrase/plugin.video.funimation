import re
from .core import Core


class Login(Core):

    def __init__(self):
        super(Login, self).__init__()
        self.logged_in = False

    def login(self):
        if self.cookie_expired:
            self._login()
        else:
            self.logged_in = True

    def _login(self):
        user = self.settings.getSetting('username')
        passwd = self.settings.getSetting('password')
        if user and passwd:
            payload = {'username': user, 'password':
                       passwd, 'sessionid': self._get_session()}

            resp = self.post('phunware/user/login.json', payload)['user']
            if len(resp['session']) > 32:
                match = re.match(r'^.*?\\"(.*)\\".*$', resp['session'])
                if match is None:
                    self.common.show_error_message('Unknown login error')
                else:
                    self.common.show_error_message(match.group(1))
            else:
                self.logged_in = True

    def _get_session(self):
        return self.get('phunware/system/connect.json')['sessid']
