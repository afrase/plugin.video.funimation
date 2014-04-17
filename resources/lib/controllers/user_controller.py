from resources.lib.http_client import HTTPClient
from resources.lib.controllers.base_controller import BaseController
from resources.lib.models.user import User


class UserController(BaseController):
    def __init__(self):
        super(UserController, self).__init__()

        self.http = HTTPClient()
        self.cookie_expired = True
        self.logged_in = False
        self.user = None

        cookies = self.http.get_cookies_str().split('Set-Cookie3: ')
        # we are ignoring expired cookies so if the ci_session cookie is in there then it's still active.
        if len(cookies) > 0:
            self.common.log('checking to see if cookie has expired', 5)
            for cookie in cookies:
                if 'ci_session' in cookie and self.cookie_expired:
                    self.common.log('cookie on file is still good', 5)
                    self.cookie_expired = False
                    self.logged_in = True

        if self.cookie_expired:
            self.common.log('cookie has expired', 5)

        self.urls = {
            'connect': 'http://www.funimation.com/phunware/system/connect.json',
            'login': 'http://www.funimation.com/phunware/user/login.json',
        }

    def login(self):
        user = self.plugin.getSetting('username')
        passwd = self.plugin.getSetting('password')
        if user and passwd and self.cookie_expired:
            self.common.log('got username and password', 5)
            self.common.log('cookie doesnt exist or has expired', 5)
            payload = {'username': user, 'password': passwd, 'sessionid': self.__get_session__()}
            resp, status = self.http.post(self.urls['login'], payload)
            if status == 200:
                self.user = User(resp['user'])
                if self.user.logged_in:
                    self.http.save()
                    return True
                else:
                    self.utils.show_error_message(self.user.error_message)
                    return False
            else:
                self.utils.show_error_message()
                return False
        else:
            return False

    def __get_session__(self):
        self.common.log('getting a session ID', 5)
        resp, status = self.http.get(self.http.urls['connect'])
        if status == 200:
            return resp['sessid']
        else:
            return None