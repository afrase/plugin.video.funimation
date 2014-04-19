from resources.lib.http_client import HTTPClient
from resources.lib.controllers.base_controller import BaseController
from resources.lib.models.user import User


class UserController(BaseController):
    def __init__(self):
        super(UserController, self).__init__()

        self.__http__ = HTTPClient()
        self.cookie_expired = True
        self.logged_in = False
        self.user = None

        self.urls = {
            'connect': 'http://www.funimation.com/phunware/system/connect.json',
            'login': 'http://www.funimation.com/phunware/user/login.json',
        }

        cookies = self.__http__.get_cookies_str().split('Set-Cookie3: ')
        # we are ignoring expired cookies so if the ci_session cookie is in there then it's still active.
        if len(cookies) > 0:
            self._common.log('checking to see if cookie has expired', 5)
            for cookie in cookies:
                if 'ci_session' in cookie and self.cookie_expired:
                    self._common.log('cookie on file is still good', 5)
                    self.cookie_expired = False
                    self.logged_in = True

        if self.cookie_expired:
            self._common.log("cookie has expired or doesn't exist", 5)

    def login(self):
        user = self._plugin.getSetting('username')
        passwd = self._plugin.getSetting('password')
        if user and passwd and self.cookie_expired:
            self._common.log('got username and password', 5)
            self._common.log('cookie doesnt exist or has expired', 5)
            payload = {'username': user, 'password': passwd, 'sessionid': self._get_session()}
            resp = self.__http__.post(self.urls['login'], payload)
            if resp:
                self.user = User(resp['user'])
                if self.user.logged_in:
                    self.__http__.save()
                    return True
                else:
                    self._utils.show_error_message(self.user.error_message)
                    return False
            else:
                self._utils.show_error_message()
                return False
        else:
            return False

    def _get_session(self):
        self._common.log('getting a session ID', 5)
        resp, status = self.__http__.get(self.__http__.urls['connect'])
        if status == 200:
            return resp['sessid']
        else:
            return None