from resources.lib.http_client import HttpClient
from resources.lib.models.user import User
from resources.lib.utils import Utils


class UserController(object):
    def __init__(self, username=None, password=None):
        utils = Utils()
        self.__req__ = HttpClient()
        self.log = utils.get_log(Utils.DEBUG)

        self.__cookie_cache__ = utils.get_cookie_cache()
        self.__user_cache__ = utils.get_user_cache()
        self.__sessionid_cache__ = utils.get_sessionid_cache()

        # no username or password was set. just get a session id
        if username and password:
            # either never logged in or cache cleared/expired
            if len(self.__cookie_cache__.items()) <= 0 and len(
                    self.__user_cache__.items()) <= 0:
                # we have no cached cookies and the username and password is set.
                # login and create the user model
                self.log('User not cached, trying to login')
                self.__login__(username, password)
            else:
                # we have a cached login. check if the cache match's the current username
                if username != self.__user_cache__['name']:
                    self.__login__(username, password)
                else:
                    # we have cookies cached, set the cookie jar to the cached cookies
                    self.__req__.update_cookie_jar(self.__cookie_cache__)
                    self.__user__ = User(self.__user_cache__)
        else:
            self.log('No login info, using anonymous')
            self.__get_session_id__()
        self.log('Logged in as %s' % self.__user__.name)

    def __get_session_id__(self, new=False):
        if not new:
            if len(self.__sessionid_cache__.items()) <= 0:
                self.log('Session ID has no cache, get one')
                self.__get_new_session_id__()
        else:
            self.log('Getting a new session ID')
            self.__get_new_session_id__()

        return self.__sessionid_cache__['sessid']

    def __get_new_session_id__(self):
        self.__sessionid_cache__.update(
            self.__req__.post('/phunware/system/connect.json').json())
        self.__sessionid_cache__.sync()

    def __login__(self, username, password):
        payload = {
            'username': username,
            'password': password,
            'sessionid': self.__get_session_id__(),
        }
        resp = self.__req__.post(
            '/phunware/user/login.json', payload
        ).json()['user']

        self.__user__ = User(resp)

        self.__user_cache__.update(self.__user__.json)
        self.__cookie_cache__.update(self.__req__.get_cookie_dict())

        self.__user_cache__.sync()
        self.__cookie_cache__.sync()